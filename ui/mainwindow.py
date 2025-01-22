import json
from pathlib import Path

from PySide6.QtCore import QTemporaryDir, QThreadPool, QUrl
from PySide6.QtGui import QAction
from PySide6.QtWebEngineCore import QWebEngineProfile, QWebEngineSettings
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (
    QFileDialog,
    QGridLayout,
    QMainWindow,
    QProgressDialog,
    QSpacerItem,
    QWidget,
)

from src.map import Map


class MainWindow(QMainWindow):
    def __init__(self, path: Path):
        super().__init__()

        self.setMinimumSize(1280, 768)
        
        self.tempdir = QTemporaryDir()
        self.menubar = self.menuBar()
        self.filemenu = self.menubar.addMenu("File")

        self.loadkmlaction = QAction("Load KML...", self)
        self.loadkmlaction.triggered.connect(self.open_kml_file)
        self.filemenu.addAction(self.loadkmlaction)

        self.reloadaction = QAction("Reload", self)
        self.reloadaction.triggered.connect(self.load_map)
        self.filemenu.addAction(self.reloadaction)

        print("loading webview...")
        self.webview = QWebEngineView()

        s = QWebEngineProfile.defaultProfile().settings()
        s.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)

        self.map = Map(51.056919, 5.1776879, 6, Path(self.tempdir.path()))
        self.map_url = QUrl().fromLocalFile(str(Path(self.tempdir.path() + "/map.html")))

        self.mainlayout = QGridLayout()
        self.widget = QWidget()
        self.widget.setLayout(self.mainlayout)
        self.setCentralWidget(self.widget)

        self.mainlayout.addWidget(self.webview)
        self.load_map()

    def load_map(self):
        self.map.save()
        self.webview.setUrl(self.map_url)
        # h = self.map.get_html()
        # self.webview.setHtml(h)
        


    def open_kml_file(self):
        path = Path(QFileDialog.getOpenFileName(self, "Open KML File", "", "KML Files (*.kml)")[0])
        if path.exists():
            print("loading kml file")
            self.map.load_placemarks(path)
            self.load_map()

