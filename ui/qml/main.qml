
import QtQuick
import QtQuick.Dialogs
import QtQuick.Controls
import QtPositioning
import QtLocation
import QtCore

Rectangle {
    id: win
    //! [GeoJsonData Creation]
    GeoJsonData {
        id: geoDatabase
        sourceUrl: dataPath
    }
    //! [GeoJsonData Creation]

    //! [MapView Creation]
    MapView {
        id: view
        anchors.fill: parent
        map.plugin: Plugin { name: "osm" }
        map.zoomLevel: 12
        map.center: QtPositioning.coordinate(49.970102, 10.418593)
    //! [MapView Creation]

        property bool autoFadeIn: false
        property variant referenceSurface: QtLocation.ReferenceSurface.Map

        //! [clearAllItems]
        function clearAllItems()
        {
            geoDatabase.clear();
        }
        //! [clearAllItems]

        //! [MapItemView]
        MapItemView {
            id: miv
            parent: view.map
            //! [MapItemView]
            //! [MapItemView Model]
            model: geoDatabase.model
            //! [MapItemView Model]
            //! [MapItemView Delegate]
            delegate: GeoJsonDelegate {}
            //! [MapItemView Delegate]
            //! [MapItemView1]
        }
        //! [MapItemView1]
        // Menu {
        //     id: mapPopupMenu

        //     property variant coordinate

        //     MenuItem {
        //         text: qsTr("Rectangle")
        //         onTriggered: view.addGeoItem("RectangleItem")
        //     }
        //     MenuItem {
        //         text: qsTr("Circle")
        //         onTriggered: view.addGeoItem("CircleItem")
        //     }
        //     MenuItem {
        //         text: qsTr("Polyline")
        //         onTriggered: view.addGeoItem("PolylineItem")
        //     }
        //     MenuItem {
        //         text: qsTr("Polygon")
        //         onTriggered: view.addGeoItem("PolygonItem")
        //     }
        //     MenuItem {
        //         text: qsTr("Clear all")
        //         onTriggered: view.clearAllItems()
        //     }

        //     function show(coordinate) {
        //         mapPopupMenu.coordinate = coordinate
        //         mapPopupMenu.popup()
        //     }
        // }

        //! [Hoverhandler Map]
        HoverHandler {
            id: hoverHandler
            property variant currentCoordinate
            grabPermissions: PointerHandler.CanTakeOverFromItems | PointerHandler.CanTakeOverFromHandlersOfDifferentType

            onPointChanged: {
                currentCoordinate = view.map.toCoordinate(hoverHandler.point.position);
            }
        }
        //! [Hoverhandler Map]

        TapHandler {
            id: tapHandler
            property variant lastCoordinate
            acceptedButtons: Qt.LeftButton | Qt.RightButton

            //! [Taphandler Map]
            onSingleTapped: (eventPoint, button) => {
                lastCoordinate = view.map.toCoordinate(tapHandler.point.position);
            }
            //! [Taphandler Map]
        }

        TapHandler {
            acceptedButtons: Qt.LeftButton | Qt.RightButton
            onDoubleTapped: (eventPoint, button) => {
                var preZoomPoint = view.map.toCoordinate(eventPoint.position);
                if (button === Qt.LeftButton)
                    view.map.zoomLevel = Math.floor(view.map.zoomLevel + 1)
                else
                    view.map.zoomLevel = Math.floor(view.map.zoomLevel - 1)
                var postZoomPoint = view.map.toCoordinate(eventPoint.position);
                var dx = postZoomPoint.latitude - preZoomPoint.latitude;
                var dy = postZoomPoint.longitude - preZoomPoint.longitude;
                view.map.center = QtPositioning.coordinate(view.map.center.latitude - dx,
                                                           view.map.center.longitude - dy);
            }
        }
    //! [MapView Creation1]
    }
}

