from pathlib import Path

from PySide6.QtCore import QTemporaryDir, QUrl
from PySide6.QtWebEngineCore import QWebEngineProfile, QWebEngineSettings
from PySide6.QtWidgets import QApplication, QFileDialog, QMainWindow

from src.map import Map
from ui.ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.main_window = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.tempdir = QTemporaryDir()

        self.map = Map(51.056919, 5.1776879, 6, Path(self.tempdir.path()))
        self.map_url = QUrl().fromLocalFile(str(Path(self.tempdir.path() + "/map.html")))

        self.ui.actionLoad_KML.triggered.connect(self.open_kml_file)
        self.ui.actionReload.triggered.connect(self.load_map)
        self.ui.actionAbout_Qt.triggered.connect(lambda: QApplication.aboutQt())
        self.ui.actionExit.triggered.connect(self.close)

        self.ui.webEngineView.loadFinished.connect(lambda: self.ui.statusbar.showMessage("ready", 5000))
        self.ui.webEngineView.loadStarted.connect(lambda: self.ui.statusbar.showMessage("loading..."))

        s = QWebEngineProfile.defaultProfile().settings()
        s.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)

        self.load_map()

    def load_map(self):
        self.map.save()
        self.ui.webEngineView.setUrl(self.map_url)

    def open_kml_file(self):
        path = Path(QFileDialog.getOpenFileName(self, "Open KML File", "", "KML Files (*.kml)")[0])
        if path.exists():
            self.map.load_placemarks(path)
            self.load_map()

