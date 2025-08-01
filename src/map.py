import multiprocessing
from pathlib import Path

import folium
from branca.element import Element
from folium.template import Template
from PySide6.QtCore import QLoggingCategory, qCDebug, qCInfo  # noqa: F401
from PySide6.QtWebChannel import QWebChannel

from src.bridge import MapBridge
from src.kml import KMLReader


class Map:
    def __init__(self, lat, lon, zoom, path: Path):
        self.lat = lat
        self.lon = lon
        self.zoom = zoom
        self.map = folium.Map(location=[lat, lon], zoom_start=zoom)
        self.kml_reader = KMLReader()
        if path.exists():
            self.path = path
        else:
            raise Exception("path does not exist")
        
        #setup webchannel
        self.webchannel = QWebChannel()
        self.map_bridge = MapBridge()
        self.webchannel.registerObject("bridge", self.map_bridge)

        # add qwebchannel js to map
        self.map.add_js_link("qwebchannel", "qrc:///qtwebchannel/qwebchannel.js")
        # add required js code 
        webchanneljs = Element("""
        <script type="text/javascript">
        
            const origStyles = new Map();
        
            //find the feature group as it gets a random name from folium
            function findFeatureGroupByPrefix(prefix = 'feature_group_') {
                for (let key in window) {
                    if (key.startsWith(prefix) && window[key] instanceof L.FeatureGroup) {
                        return window[key];
                    }
                }
                return null;
            }

            function highlightPolygonByName(name) {

                // TODO: this should only run the first time the map is loaded
                const fg = findFeatureGroupByPrefix();
                if (!fg) { 
                    console.error("Feature group not found"); 
                    return;
                }
                fg.eachLayer(function(layer) {
                    if (layer.getTooltip && layer.getTooltip()) {
                        let tooltip = layer.getTooltip().getContent();
                        if (tooltip && tooltip.includes(name) && layer.setStyle) {
                            if (!origStyles.has(layer)) {
                                origStyles.set(layer, {
                                    ...layer.options
                                });
                            }
                            layer.setStyle({ weight: 10, opacity: 1, color: 'magenta'});
                        }
                    }
                });
            }

            function resetHighlight() {
                origStyles.forEach((style, layer) => {
                    if (layer.setStyle) {
                        layer.setStyle(style);
                    }
                });
                origStyles.clear();
            }

            // set up webchannel
            window.onload = function() {
                console.log("setting up webchannel...");
                new QWebChannel(qt.webChannelTransport, function(channel) {
                    window.bridge = channel.objects.bridge;

                    bridge.highlight_region_signal.connect(function(region_name) {
                        highlightPolygonByName(region_name);
                        console.log("highlighted regions: " + region_name);
                    });

                    bridge.reset_highlight_signal.connect(function() {
                        console.log("resetting highlight");
                        resetHighlight();
                    });
                });
            };
        </script>
        """)
        self.map.get_root().header.add_child(webchanneljs)

        self.log_category = QLoggingCategory("map")
        
        multiprocessing.freeze_support()


    def save(self, progress_callback):
        # ? is there a way to speed this up?
        qCInfo(self.log_category, 'saving...')
        self.map.save(str(Path(self.path / "map.html")))
        qCInfo(self.log_category, 'saved')

    def get_html(self):
        return self.map.get_root().render()
    
    def load_placemarks(self, kml_path, progress_callback):
        progress_callback.emit("")

        self.kml_reader.loadKML(kml_path, progress_callback)

        # TODO: create seperate feature groups for each folder in the kml 
        fg = CustomFeatureGroup(name="placemarks", control=False).add_to(self.map)

        progress_callback.emit("adding elements...")
        
        # TODO: just execute everything in one thread if there aren't that many placemarks (>500 or smth, will have to test), since starting the processes usually takes longer than the loading itself

        with multiprocessing.Manager() as manager:
            points = manager.list([])
            polygons = manager.list([])

            p1 = multiprocessing.Process(name="points", target=self.kml_reader.getPoints, args=(points, ))
            p2 = multiprocessing.Process(name="polygons", target=self.kml_reader.getPolygons, args=(polygons, ))

            p1.start()
            p2.start()

            p2.join()
            p1.join()

            # add points to map as markers
            qCInfo(self.log_category, f"adding {len(points)} points...")
            for i, point in enumerate(points):
                folium.Marker(location=[point[0], point[1]], tooltip=point[2], popup=point[3]).add_to(fg)

            # add polygons to map
            qCInfo(self.log_category, f"adding {len(polygons)} polygons...")
            for i, polygon in enumerate(polygons):
                folium.Polygon(locations=polygon[0], color=f"#{polygon[3][0]}", fill_color=f"#{polygon[4]}", weight=polygon[3][1], tooltip=polygon[1], popup=polygon[2], fillOpacity=0.5).add_to(fg)

        qCInfo(self.log_category, "done")

class CustomFeatureGroup(folium.FeatureGroup):
    
    _template = Template(
        """
        {% macro script(this, kwargs) %}
            var {{ this.get_name() }} = L.featureGroup(
                {{ this.options|tojavascript }}
            )
            .on('click', function(ev) { 
                bridge.region_clicked(ev.sourceTarget.getTooltip().getContent());
            });
        {% endmacro %}
        """
    )