import shutil
from pathlib import Path

from PySide6.QtCore import QTemporaryDir, QThreadPool, QUrl
from PySide6.QtWebEngineCore import QWebEngineProfile, QWebEngineSettings
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QProgressDialog,
)

from src.map import Map
from src.worker import Worker
from ui.ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.tempdir = QTemporaryDir()
        self.threadpool = QThreadPool()

        # init map and save url for loading later
        self.map = Map(51.056919, 5.1776879, 6, Path(self.tempdir.path()))
        self.map_url = QUrl().fromLocalFile(str(Path(self.tempdir.path() + "/map.html")))

        # setup actions
        self.ui.actionLoad_KML.triggered.connect(self.open_kml_file)
        self.ui.actionReload.triggered.connect(self.load_map)
        self.ui.actionAbout_Qt.triggered.connect(lambda: QApplication.aboutQt())
        self.ui.actionExit.triggered.connect(self.close)

        self.ui.webEngineView.loadFinished.connect(lambda: self.ui.statusbar.showMessage("ready", 5000))
        self.ui.webEngineView.loadStarted.connect(lambda: self.ui.statusbar.showMessage("loading..."))

        # allow webengine to load external content, needed for leaflet
        s = QWebEngineProfile.defaultProfile().settings()
        s.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)

        self.load_map()

    def load_map(self):
        self.map.save()
        # copy html here for debugging
        shutil.copy(str(Path(self.tempdir.path() + "/map.html")), str(Path("./")))
        self.ui.webEngineView.setUrl(self.map_url)

    def open_kml_file(self):
        def progress_callback(value, message):
            # print(value, message)
            if value != 0 and pbar.maximum() == 0:
                pbar.setMaximum(100)
            pbar.setValue(value)
            if message != "":
                pbar.setLabelText(message)

        def finished():
            print("thread finished")
            self.load_map()
            pbar.close()
        
        path = Path(QFileDialog.getOpenFileName(self, "Open KML File", "", "KML Files (*.kml)")[0])
        if path.exists():
            # clear webengineview
            self.ui.webEngineView.setUrl("about:blank")
            # re-init map
            # self.map = Map(51.056919, 5.1776879, 6, Path(self.tempdir.path()))
            pbar = QProgressDialog("Loading KML...", "", 0, 0, self)
            pbar.setWindowTitle("Loading KML...")
            pbar.setCancelButton(None)
            pbar.setMinimumWidth(400)
            pbar.show()
            # load kml in seperate thread to not block event loop
            worker = Worker(self.map.load_placemarks, path)
            worker.signals.progress.connect(progress_callback)
            worker.signals.finished.connect(finished)

            self.threadpool.start(worker)
            # self.map.load_placemarks(path)



