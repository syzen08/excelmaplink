import QtQuick
import QtLocation
import QtPositioning

Rectangle {
    id: main
    color: 'black'
    
    Plugin {
        id: mapPlugin
        name: "osm"
    }

    Map {
        id: map
        
        anchors.fill: parent
        plugin: mapPlugin
        center: QtPositioning.coordinate(49.970102, 10.418593)
        zoomLevel: 14
        property geoCoordinate startCentroid

        MapPolygon {
            color: 'green'
            opacity: 0.3
            path: [
                { latitude: 49.977051, longitude: 10.405334 },
                { latitude: 49.975664, longitude: 10.434563 },
                { latitude: 49.960786, longitude: 10.419401 }
            ]
        }

        WheelHandler {
            id: wheel
            // workaround for QTBUG-87646 / QTBUG-112394 / QTBUG-112432:
            // Magic Mouse pretends to be a trackpad but doesn't work with PinchHandler
            // and we don't yet distinguish mice and trackpads on Wayland either
            acceptedDevices: Qt.platform.pluginName === "cocoa" || Qt.platform.pluginName === "wayland"
                            ? PointerDevice.Mouse | PointerDevice.TouchPad
                            : PointerDevice.Mouse
            rotationScale: 1/120
            property: "zoomLevel"
        }
        DragHandler {
            id: drag
            target: null
            onTranslationChanged: (delta) => map.pan(-delta.x, -delta.y)
        }
    }

}

