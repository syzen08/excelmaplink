import shutil
from pathlib import Path

from PySide6.QtCore import (
    QLoggingCategory,
    Qt,
    QTemporaryDir,
    QThreadPool,
    QUrl,
    qCDebug,
    qCInfo,
    qCWarning,
)
from PySide6.QtWebEngineCore import QWebEngineProfile, QWebEngineSettings
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QFileDialog,
    QMainWindow,
)

from src.excel import Spreadsheet
from src.map import Map
from src.worker import Worker
from ui.mainwindow_ui import Ui_MainWindow
from ui.progressDialog_ui import Ui_progressDialog
from ui.settingsDialog_ui import Ui_settingsDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.log_category = QLoggingCategory("mainwindow")

        qCDebug(self.log_category, "loading ui...")
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.tempdir = QTemporaryDir()
        self.threadpool = QThreadPool()

        self.spreadsheet = None

        # init map and save url for loading later
        qCDebug(self.log_category, "initializing map...")
        self.map = Map(51.056919, 5.1776879, 6, Path(self.tempdir.path()))
        self.map_url = QUrl().fromLocalFile(str(Path(self.tempdir.path() + "/map.html")))
        self.map.core.receivedText.connect(self.clicked_in_map)

        # set up actions
        self.ui.actionLoad_KML.triggered.connect(self.open_kml_file)
        self.ui.actionReload.triggered.connect(self.load_map)
        self.ui.actionAbout_Qt.triggered.connect(lambda: QApplication.aboutQt())
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionOpen_Excel.triggered.connect(self.openExcelFile)

        self.ui.webEngineView.loadFinished.connect(lambda: self.ui.statusbar.showMessage("ready", 5000))
        self.ui.webEngineView.loadStarted.connect(lambda: self.ui.statusbar.showMessage("loading..."))

        # allow webengine to load external content, needed for leaflet
        s = QWebEngineProfile.defaultProfile().settings()
        s.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        qCDebug(self.log_category, "loading map...")
        self.load_map()

    def load_map(self):
        def finished():
            # copy html here for debugging
            # shutil.copy(str(Path(self.tempdir.path() + "/map.html")), str(Path("./")))
            self.setCursor(Qt.CursorShape.ArrowCursor)
            self.ui.webEngineView.setUrl(self.map_url)
        
        qCInfo(self.log_category, "saving map...")
        self.ui.statusbar.showMessage("saving map...")
        worker = Worker(self.map.save)
        worker.signals.finished.connect(finished)
        self.setCursor(Qt.CursorShape.WaitCursor)
        self.threadpool.start(worker)

    def open_kml_file(self):
        def progress_callback(message):
            if message != "":
                pbarui.message.setText(message)

        def finished():
            qCInfo(self.log_category, "loading thread finished")
            self.setCursor(Qt.CursorShape.ArrowCursor)
            self.load_map()
            pbar.close()
        
        qCDebug(self.log_category, "open_kml_file triggered")
        path = Path(QFileDialog.getOpenFileName(self, "Open KML File", "", "KML Files (*.kml)")[0])
        if path.exists():
            qCInfo(self.log_category, "starting loading of kml...")
            # clear webengineview
            self.ui.webEngineView.setUrl("about:blank")
            # re-init map
            # self.map = Map(51.056919, 5.1776879, 6, Path(self.tempdir.path()))
            pbarui = Ui_progressDialog()
            pbar = QDialog(self)
            pbarui.setupUi(pbar)
            pbarui.progressBar.setRange(0, 0)
            pbar.show()
            # load kml in seperate thread to not block event loop
            worker = Worker(self.map.load_placemarks, path)
            worker.signals.progress.connect(progress_callback)
            worker.signals.finished.connect(finished)

            self.setCursor(Qt.CursorShape.WaitCursor)
            self.threadpool.start(worker)
            # self.map.load_placemarks(path)

    def clicked_in_map(self, data: str):
        qCDebug(self.log_category, f"data: |{data}|")
        if data.startswith("click&"):
            self.ui.statusbar.showMessage(f"clicked on: {data[6:]}", 5000)
            self.spreadsheet.toggle_region(data[6:])
        else:
            self.ui.statusbar.showMessage(f"received data: {data}", 5000)

    def openExcelFile(self):
        path = Path(QFileDialog.getOpenFileName(self, "Open Excel File", "", "Excel Files (*.xlsx *.xls)")[0])
        if path.exists():
            qCInfo(self.log_category, f"opening excel file: {path}")
            # TODO: get these values from a config instead of hardcoding them
            self.spreadsheet = Spreadsheet(path, self.show_settings_dialog)
            
    def show_settings_dialog(self):
        qCDebug(self.log_category, "showing settings dialog")
        dialog = QDialog(self)
        ui = Ui_settingsDialog()
        ui.setupUi(dialog)
        ui.buttonBox.accepted.connect(dialog.accept)
        if dialog.exec():
            settings = {
                "region_sheet": ui.tourSheetNameLineEdit.text(),
                "region_map_name_column": ui.tourSheetMapNameColumnLineEdit.text(),
                "region_sheet_start_row": ui.tourSheetStartRowSpinBox.value(),
                "region_name_column": ui.tourSheetTourNameLineEdit.text(),
                "calc_sheet": ui.calcSheetNameLineEdit.text(),
                "calc_column": ui.calcSheetColumnLineEdit.text(),
                "calc_range": f"{ui.fromSpinbox.value()}@@{ui.toSpinbox.value()}",
                "save_map_path": ui.saveMapLocationCheckBox.isChecked()
            }
            qCDebug(self.log_category, f"settings: {settings}")
            return settings
        else:
            qCWarning(self.log_category, "settings dialog cancelled, idk what to do now")
            raise NotImplementedError("settings dialog was cancelled")

