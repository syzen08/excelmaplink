import QtQuick
import QtQuick.Dialogs
import QtQuick.Controls
import QtLocation
import QtPositioning
import QtQuick.Layouts
import QtQml

ApplicationWindow {
    id: applicationWindow

    required property url dataPath

    title: qsTr("excelmaplink")
    width: 800
    height: 600
    visible: true

    onDataPathChanged: {console.log(dataPath);}

    Action {
        id: quitAction
        text: qsTr("Quit")
        shortcut: StandardKey.Close
        onTriggered: applicationWindow.close()
    }

    Action {
        id: openGeoJsonAction
        text: qsTr("Open GeoJSON...")
        onTriggered: {
            geoJsonFileDialog.open()
        }
    }

    FileDialog {
        visible: false
        id: geoJsonFileDialog
        title: "choose geojson"
        fileMode: FileDialog.OpenFile
        nameFilters: ["GeoJSON files (*.geojson *.json)"]
        onAccepted: {
            geoDatabase.sourceUrl = geoJsonFileDialog.selectedFile;
            console.log(geoJsonFileDialog.selectedFile)
        }
    }

    menuBar: MenuBar {
        id: mainMenu
        Menu {
            id: fileMenu
            title: qsTr("File")

            MenuItem{
                action: openGeoJsonAction
            }

            MenuSeparator{
            }

            MenuItem {
                action: quitAction
            }
        }

    }

        Map {
            id: map
            center: QtPositioning.coordinate(51.165691, 10.451526)
            zoomLevel: 6
            plugin: Plugin { name: "osm" }
            property variant referenceSurface: QtLocation.ReferenceSurface.Map
            anchors.fill: parent
            

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

            MapItemView {
                id: miv
                model: geoDatabase.model
                delegate: GeoJsonDelegate {}
            }
            
            onMapReadyChanged: {console.log("map ready")}
    }

    GeoJsonData {
        id: geoDatabase
        sourceUrl: applicationWindow.dataPath
    }

}