import time
from pathlib import Path

import folium
from branca.element import Element
from folium.template import Template
from PySide6.QtNetwork import QHostAddress, QSslSocket
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWebSockets import QWebSocketServer

from src.kml import KMLReader
from src.webchannel.core import Core
from src.webchannel.websocketclientwrapper import WebSocketClientWrapper


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
        
        # set up web channel for communication between the map and this program.
        # taken from https://doc.qt.io/qtforpython-6/examples/example_webchannel_standalone.html#example-webchannel-standalone
        if not QSslSocket.supportsSsl():
            raise("No SSL support detected")
            
        self.server = QWebSocketServer("QWebChannel Server",
                                       QWebSocketServer.SslMode.NonSecureMode)
        # start server and check if its running
        if not self.server.listen(QHostAddress.SpecialAddress.LocalHost, 12345):
            raise("Failed to start web socket server")
        
        self.client_wrapper = WebSocketClientWrapper(self.server)

        self.channel = QWebChannel()
        self.client_wrapper.client_connected.connect(self.channel.connectTo)

        self.core = Core()
        self.channel.registerObject("core", self.core)

        # add qwebchannel js to map
        self.map.add_js_link("qwebchannel", "qrc:///qtwebchannel/qwebchannel.js")
        # add required js code 
        webchanneljs = Element("""
        <script type="text/javascript">
            //BEGIN SETUP
            window.onload = function() {
                if (location.search != "")
                    var baseUrl = (/[?&]webChannelBaseUrl=([A-Za-z0-9\-:/\.]+)/.exec(location.search)[1]);
                else
                    var baseUrl = "ws://localhost:12345";

                console.info("Connecting to WebSocket server at " + baseUrl + ".");
                var socket = new WebSocket(baseUrl);

                socket.onclose = function() {
                    console.error("web channel closed");
                };
                socket.onerror = function(error) {
                    console.error("web channel error: " + error);
                };
                socket.onopen = function() {
                    console.info("WebSocket connected, setting up QWebChannel.");
                    new QWebChannel(socket, function(channel) {
                        // make core object accessible globally
                        window.core = channel.objects.core;
                        core.receiveText("Client connected, ready to send/receive messages!");
                    });
                }
            }
            //END SETUP
        </script>
        """)
        self.map.get_root().header.add_child(webchanneljs)


    def save(self):
        # ? is there a way to speed this up?
        self.map.save(str(Path(self.path / "map.html")))

    def get_html(self):
        return self.map.get_root().render()
    
    def load_placemarks(self, kml_path, progress_callback = None):
        # TODO: all these ifs look like shit, find a better way to do this
        if progress_callback:
            progress_callback.emit(0, "")
        self.kml_reader.loadKML(kml_path, progress_callback)
        # TODO: create seperate feature groups for each folder in the kml 
        fg = CustomFeatureGroup(name="placemarks", control=False).add_to(self.map)

        # TODO: launch thread for each type of placemark (point, polygon, etc.)
        # get all points from the kml
        print("getting points...") 
        if progress_callback:
            progress_callback.emit(45, "getting points...")
        points = self.kml_reader.getPoints()
        if progress_callback:
            progress_callback.emit(50, "")
        # add points to map as markers
        print(f"adding {len(points)} points...")
        for i, point in enumerate(points):
            folium.Marker(location=[point[0], point[1]], tooltip=point[2], popup=point[3]).add_to(fg)
            if progress_callback:
                progress_callback.emit(50 + int((i + 1) / len(self.kml_reader.placemarks) * 50), "")
        
        # get all polygons from the kml
        print("getting polygons...")
        if progress_callback:
            progress_callback.emit(50, "loading polygons...")

        # expected format: (list[float point], String: name, String: description, (String lineColor, int lineWidth), String fillColor)
        polygons = self.kml_reader.getPolygons(progress_callback=progress_callback, point_length=len(points))
        if progress_callback:
            progress_callback.emit(75, "adding polygons...")
        # add polygons to map
        print(f"adding {len(polygons)} polygons...")
        for i, polygon in enumerate(polygons):
            folium.Polygon(locations=polygon[0], color=f"#{polygon[3][0]}", fill_color=f"#{polygon[4]}", weight=polygon[3][1], tooltip=polygon[1], popup=polygon[2], fillOpacity=0.5).add_to(fg)
            if i % 200 == 0:
                if progress_callback:
                    progress_callback.emit(75 + int(((i + 1) / len(self.kml_reader.placemarks) + len(points) / len(self.kml_reader.placemarks)) * 25), "")
        print("done")
        if progress_callback:
            progress_callback.emit(100, "finished")
        time.sleep(0.5) # wait for all signals to fire

class CustomFeatureGroup(folium.FeatureGroup):
    
    _template = Template(
        """
        {% macro script(this, kwargs) %}
            var {{ this.get_name() }} = L.featureGroup(
                {{ this.options|tojavascript }}
            )
            .on('click', function(ev) { core.receiveText(ev.sourceTarget.getTooltip().getContent()); });
        {% endmacro %}
        """
    )