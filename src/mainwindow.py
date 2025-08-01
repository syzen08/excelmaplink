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
    QMessageBox,
)

from src.excel.spreadsheet import Spreadsheet
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
        self.ui.webEngineView.page().setWebChannel(self.map.webchannel)
        self.map.map_bridge.region_clicked_signal.connect(self.clicked_in_map)

        # set up actions
        self.ui.actionLoad_KML.triggered.connect(lambda: self.open_kml_file(self.select_kml_file()))
        # self.ui.actionLoad_KML.setVisible(False)
        self.ui.actionReload.triggered.connect(self.load_map)
        self.ui.actionAbout_Qt.triggered.connect(lambda: QApplication.aboutQt())
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionOpen_Excel.triggered.connect(self.openExcelFile)
        self.ui.actionReset_Highlight.triggered.connect(self.reset_highlight)
        self.ui.actionShow_Statusbar.toggle()
        self.ui.actionWorkbook_Settings.triggered.connect(lambda: self.show_settings_dialog(self.spreadsheet.config))

        self.ui.webEngineView.loadFinished.connect(lambda: self.ui.statusbar.showMessage("ready", 5000))
        self.ui.webEngineView.loadStarted.connect(lambda: self.ui.statusbar.showMessage("loading..."))

        # allow webengine to load external content, needed for leaflet
        s = QWebEngineProfile.defaultProfile().settings()
        s.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        qCDebug(self.log_category, "loading map...")
        self.load_map()

    def reset_highlight(self):
        self.map.map_bridge.reset_highlight()

    def load_map(self):
        def finished():
            self.setCursor(Qt.CursorShape.ArrowCursor)
            self.ui.webEngineView.setUrl(self.map_url)
        
        qCInfo(self.log_category, "saving map...")
        self.ui.statusbar.showMessage("saving map...")
        worker = Worker(self.map.save)
        worker.signals.finished.connect(finished)
        self.setCursor(Qt.CursorShape.WaitCursor)
        self.threadpool.start(worker)

    def select_kml_file(self):
        path, _ = QFileDialog.getOpenFileName(self, self.tr("Select KML File"), "", self.tr("KML Files (*.kml)"))
        if path and Path(path).exists() and Path(path).is_file():
            return Path(path)
        else:
            return None

    def open_kml_file(self, path: Path):
        def progress_callback(message):
            if message != "":
                pbarui.message.setText(message)

        def finished():
            qCInfo(self.log_category, "loading thread finished")
            self.setCursor(Qt.CursorShape.ArrowCursor)
            self.load_map()
            pbar.close()
        
        qCDebug(self.log_category, "open_kml_file triggered")
        qCInfo(self.log_category, f"starting loading of kml... (path: {path})")
        # clear webengineview
        self.ui.webEngineView.setUrl("about:blank")
        self.reset_map()
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

    def clicked_in_map(self, data: str):
        qCDebug(self.log_category, f"data: |{data}|")
        self.ui.statusbar.showMessage(f"clicked on: {data}", 5000)
        self.spreadsheet.toggle_region(data)
            
        if self.ui.actionHighlighting_Test.isChecked():
            self.map.map_bridge.highlight_region(data)

    def openExcelFile(self):
        path = Path(QFileDialog.getOpenFileName(self, self.tr("Open Excel File"), "", self.tr("Excel Files (*.xlsx *.xls)"))[0])
        if path.exists() and path.is_file():
            qCInfo(self.log_category, f"opening excel file: {path}")
            if self.spreadsheet:
                self.spreadsheet.__del__()  # close the old spreadsheet if it exists
            self.spreadsheet = Spreadsheet(path, self)
            self.ui.actionWorkbook_Settings.setEnabled(True)
            
    def reset_map(self):
        self.map = Map(51.056919, 5.1776879, 6, Path(self.tempdir.path()))
        self.ui.webEngineView.page().setWebChannel(self.map.webchannel)
        self.map.map_bridge.region_clicked_signal.connect(self.clicked_in_map)
            
    def show_settings_dialog(self, settings: dict = None):
        tempmap = None
        def validate_kml_path():
            if ui.saveMapLocationCheckBox.isChecked() and (Path(ui.mapLocationLineEdit.text()).exists() and Path(ui.mapLocationLineEdit.text()).is_file()):
                dialog.accept()
            elif not ui.saveMapLocationCheckBox.isChecked():
                tempmap = self.select_kml_file() #BUG: make this actually store in the settings dict, that would be nice
                if not tempmap:
                    QMessageBox.critical(self, self.tr("Missing Map Location"), self.tr("Please select a valid map to open."))
                    validate_kml_path()
                    return
                dialog.accept()
            else:
                QMessageBox.critical(self, self.tr("Missing Map Location"), self.tr("Please select a valid map using the 'Select File...' Button."))
        qCDebug(self.log_category, "showing settings dialog")
        dialog = QDialog(self)
        ui = Ui_settingsDialog()
        ui.setupUi(dialog)
        if settings:
            ui.tourSheetNameLineEdit.setText(settings["region_sheet"].get_value())
            ui.tourSheetMapNameColumnLineEdit.setText(settings["region_map_name_column"].get_value())
            ui.tourSheetStartRowSpinBox.setValue(settings["region_sheet_start_row"].get_value())
            ui.tourSheetTourNameLineEdit.setText(settings["region_name_column"].get_value())
            ui.calcSheetNameLineEdit.setText(settings["calc_sheet"].get_value())
            ui.calcSheetColumnLineEdit.setText(settings["calc_column"].get_value())
            ui.fromSpinbox.setValue(settings["calc_range"].get_value()[0])
            ui.toSpinbox.setValue(settings["calc_range"].get_value()[1])
            ui.saveMapLocationCheckBox.setChecked(settings["save_map_path"].get_value())
            ui.mapLocationLineEdit.setText(settings["linked_map"].get_value())
        ui.buttonBox.accepted.connect(validate_kml_path)
        ui.mapLocationButton.clicked.connect(lambda: ui.mapLocationLineEdit.setText(str(self.select_kml_file())))
        if dialog.exec():
            new_settings = {
                "region_sheet": ui.tourSheetNameLineEdit.text(),
                "region_map_name_column": ui.tourSheetMapNameColumnLineEdit.text(),
                "region_sheet_start_row": ui.tourSheetStartRowSpinBox.value(),
                "region_name_column": ui.tourSheetTourNameLineEdit.text(),
                "calc_sheet": ui.calcSheetNameLineEdit.text(),
                "calc_column": ui.calcSheetColumnLineEdit.text(),
                "calc_range": (ui.fromSpinbox.value(), ui.toSpinbox.value()),
                "save_map_path": ui.saveMapLocationCheckBox.isChecked(),
                "linked_map": ui.mapLocationLineEdit.text(),
                "temp_map": tempmap if ui.saveMapLocationCheckBox.isChecked() else None
            }
            qCDebug(self.log_category, f"settings: {new_settings}")
            if settings:
                if self.spreadsheet:
                    self.spreadsheet.load_config(new_settings)
            return new_settings
        else:
            qCWarning(self.log_category, "settings dialog cancelled, idk what to do now")
            raise NotImplementedError("settings dialog was cancelled")

