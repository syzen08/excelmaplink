import json
from pathlib import Path

from PySide6.QtCore import QTemporaryDir, QUrl
from PySide6.QtGui import QAction
from PySide6.QtQuickWidgets import QQuickWidget
from PySide6.QtWidgets import (
    QFileDialog,
    QGridLayout,
    QMainWindow,
    QSpacerItem,
    QWidget,
)

from src import importkml


class MainWindow(QMainWindow):
    def __init__(self, path: Path):
        super().__init__()

        self.setMinimumSize(1280, 768)
        

        self.menubar = self.menuBar()
        self.filemenu = self.menubar.addMenu("File")

        self.loadkmlaction = QAction("Load KML...", self)
        self.loadkmlaction.triggered.connect(self.open_kml_file)
        self.filemenu.addAction(self.loadkmlaction)

        self.qtquick = None


        self.mainlayout = QGridLayout()
        self.widget = QWidget()
        self.widget.setLayout(self.mainlayout)
        self.setCentralWidget(self.widget)

        # placeholder widgets
        self.spacerL = QSpacerItem(200, 0)
        self.mainlayout.addItem(self.spacerL, 0, 1)

        self.url = self.open_kml_file(path)

        self.reloadMap()

        
        
    def reloadMap(self):
        if self.qtquick:
            self.qtquick.destroy()
        self.qtquick = QQuickWidget()
        self.qtquick.setResizeMode(QQuickWidget.SizeRootObjectToView)
        self.qtquick.rootContext().setContextProperty("dataPath", self.url)
        self.qtquick.setSource(QUrl.fromLocalFile(str(Path("./ui/qml/main.qml"))))
        self.mainlayout.addWidget(self.qtquick, 0, 0)
        if not self.qtquick.rootObject():
            raise Exception("Failed to load QML")

    def open_kml_file(self, path: Path = None) -> QUrl:
        if path is None or path is False:
            kmlfile = Path(QFileDialog.getOpenFileName(self, "Open KML File", "", "KML Files (*.kml)")[0])
        else:
            kmlfile = path

        print(kmlfile)

        self.temp_dir = QTemporaryDir()
        if (self.temp_dir.isValid()):
            geojson_path = Path(self.temp_dir.path() + "/" + kmlfile.stem + ".geojson")
            geojson = importkml.convert_kml_to_geojson(kmlfile)
            with open(geojson_path, "w") as f:
                json.dump(geojson, f)
        else:
            raise Exception("Failed to create temporary directory")
        url = QUrl.fromLocalFile(str(geojson_path))
        print(url.toString())
        self.url = url
        self.reloadMap()
        return url


        