import logging
import multiprocessing
from pathlib import Path

import folium
from branca.element import Element
from folium.template import Template
from PySide6.QtCore import QCoreApplication  # noqa: F401
from PySide6.QtWebChannel import QWebChannel

from src.bridge import MapBridge
from src.kml import KMLReader


class Map:
    
    def __init__(self, lat, lon, zoom, path: Path):
        self.logger = logging.getLogger("eml.map")
        self.lat = lat
        self.lon = lon
        self.zoom = zoom
        self.map = folium.Map(location=[lat, lon], zoom_start=zoom)
        self.kml_reader = KMLReader()
        if path.exists():
            self.path = path
        else:
            raise FileNotFoundError("path does not exist")
        
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
                    bridge.finished_loading();
                });
            };
        </script>
        """)
        self.map.get_root().header.add_child(webchanneljs)


    def save(self, progress_callback):
        # ? is there a way to speed this up?
        self.logger.info('saving...')
        self.map.save(str(Path(self.path / "map.html")))
        self.logger.info('saved')

    def get_html(self):
        return self.map.get_root().render()
    
    def load_placemarks(self, kml_path: Path, progress_callback):
        MULTIPROCESS_THRESHOLD = 300
        progress_callback.emit("")

        self.kml_reader.loadKML(kml_path, progress_callback)

        fg = CustomFeatureGroup(name="placemarks", control=False).add_to(self.map)

        progress_callback.emit(QCoreApplication.translate("Map", "adding elements..."))
        
        if len(self.kml_reader.placemarks) > MULTIPROCESS_THRESHOLD:
            self.logger.debug(f"more than {MULTIPROCESS_THRESHOLD} placemarks, getting placemarks using multiprocessing")
            with multiprocessing.Manager() as manager:
                m_points = manager.list([])
                m_polygons = manager.list([])

                p1 = multiprocessing.Process(name="points", target=self.kml_reader.getPoints, args=(m_points, ))
                p2 = multiprocessing.Process(name="polygons", target=self.kml_reader.getPolygons, args=(m_polygons, ))

                self.logger.debug("starting processes...")
                p1.start()
                p2.start()

                p2.join()
                p1.join()
                self.logger.debug("processes finished")
                
                points = []
                polygons = []
                # there's a better way, but idk
                for p in m_points:
                    points.append(p)
                for p in m_polygons:
                    polygons.append(p)
        else:
            self.logger.debug(f"less than {MULTIPROCESS_THRESHOLD} placemarks, getting placemarks synchronously")
            points = []
            polygons = []
            points = self.kml_reader.getPoints(points, True)
            polygons = self.kml_reader.getPolygons(polygons, True)

        # add points to map as markers
        self.logger.info(f"adding {len(points)} points...")
        for i, point in enumerate(points):
            if point[5] is not None:
                if point[4].startswith("custom: "):
                    self.logger.warning(f"unsupported icon found! ({point[4][7:]}). tinting is not supported, position/size may be off.")
                    icon = folium.CustomIcon(point[4][7:])
                elif point[4] == "default":
                    icon = None
                else:
                    self.logger.debug(f"icon {point[4]} with color {point[5]}")
                    icon = folium.Icon(color="black", icon_color=f"#{point[5]}", icon=point[4], prefix="fa")
            else:
                icon = None
            folium.Marker(location=[point[0], point[1]], tooltip=point[2], popup=point[3], icon=icon).add_to(fg)
        # add polygons to map
        self.logger.info(f"adding {len(polygons)} polygons...")
        for i, polygon in enumerate(polygons):
            folium.Polygon(locations=polygon[0], color=f"#{polygon[3][0]}", fill_color=f"#{polygon[4]}", weight=polygon[3][1], tooltip=polygon[1], popup=polygon[2], fillOpacity=0.5).add_to(fg)

        self.logger.info("done")

class CustomFeatureGroup(folium.FeatureGroup):
    
    _template = Template(
        """
        {% macro script(this, kwargs) %}
            var {{ this.get_name() }} = L.featureGroup(
                {{ this.options|tojavascript }}
            )
            .on('click', function(ev) {
                if (ev.sourceTarget instanceof L.Polygon) { 
                    bridge.region_clicked(ev.sourceTarget.getTooltip().getContent());
                }
            });
        {% endmacro %}
        """
    )