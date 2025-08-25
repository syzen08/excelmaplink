import contextlib
import logging
import shutil
from pathlib import Path

from PySide6.QtCore import (
    Qt,
    QTemporaryDir,
    QThreadPool,
    QUrl,
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
from src.version.commit import get_commit
from src.version.version import VERSION
from src.worker import Worker
from ui.aboutDialog_ui import Ui_aboutDialog
from ui.mainwindow_ui import Ui_MainWindow
from ui.progressDialog_ui import Ui_progressDialog
from ui.settingsDialog_ui import Ui_settingsDialog


class MainWindow(QMainWindow):
    def __init__(self, debug: bool):
        super().__init__()
        
        # set up logging
        self.logger = logging.getLogger("eml.mainwindow")
        self.logger.debug("loading ui...")
        
        self.logger.debug(f"debug: {debug}")
        self.debug = debug
        
        # setup ui
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # init things we need
        self.tempdir = QTemporaryDir()
        self.threadpool = QThreadPool()
        self.spreadsheet = None

        # init map and save url for loading later
        self.logger.debug("initializing map...")
        self.map = Map(51.165691, 10.451526, 6, Path(self.tempdir.path()))
        self.map_url = QUrl().fromLocalFile(str(Path(self.tempdir.path() + "/map.html")))
        # set the webchannel and connect it's signals up
        self.ui.webEngineView.page().setWebChannel(self.map.webchannel)
        self.map.map_bridge.region_clicked_signal.connect(self.clicked_in_map)

        # connect actions to code
        self.ui.actionLoad_KML.triggered.connect(lambda: self.open_kml_file(self.select_kml_file()))
        self.ui.actionReload.triggered.connect(self.load_map)
        self.ui.actionAbout_Qt.triggered.connect(lambda: QApplication.aboutQt())
        self.ui.actionAbout.triggered.connect(self.show_about_dialog)
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionOpen_Excel.triggered.connect(self.openExcelFile)
        self.ui.actionReset_Highlight.triggered.connect(self.reset_highlight)
        self.ui.actionWorkbook_Settings.triggered.connect(lambda: self.show_settings_dialog(self.spreadsheet.config))
        self.ui.actionCopy_Map.triggered.connect(lambda: shutil.copy(str(Path(self.tempdir.path() + "/map.html")), str(Path("./"))))
        # toggle the statusbar so it's hidden by default
        self.ui.actionShow_Statusbar.toggle()

        self.ui.webEngineView.loadFinished.connect(lambda: self.ui.statusbar.showMessage("ready", 5000))
        self.ui.webEngineView.loadStarted.connect(lambda: self.ui.statusbar.showMessage("loading..."))

        # if not in debug mode, remove the debug menu
        if not self.debug:
            self.ui.menubar.removeAction(self.ui.menuDebug.menuAction())

        # allow webengine to load external content, needed for leaflet
        s = QWebEngineProfile.defaultProfile().settings()
        s.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        
        self.logger.debug("loading map...")
        self.load_map()
        
    def closeEvent(self, event):
        # only prompt user if excel is open
        if self.spreadsheet:
            btn = QMessageBox.question(
                self, 
                self.tr("Save Excel?"), 
                self.tr("Do you want to save the workbook?"), 
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel,
                QMessageBox.StandardButton.Cancel
            )
            if btn == QMessageBox.StandardButton.Cancel:
                event.ignore()
                return None
            self.spreadsheet.wb.save()
        
        return super().closeEvent(event)

    def reset_highlight(self):
        self.map.map_bridge.reset_highlight()

    def load_map(self):
        def finished():
            self.setCursor(Qt.CursorShape.ArrowCursor)
            self.ui.webEngineView.setUrl(self.map_url)
        
        self.logger.info("saving map...")
        self.ui.statusbar.showMessage("saving map...")
        worker = Worker(self.map.save)
        worker.signals.finished.connect(finished)
        self.setCursor(Qt.CursorShape.WaitCursor)
        self.threadpool.start(worker)

    def select_kml_file(self) -> Path | None:
        """show file select dialog for kml/kmz files and then check if it's valid. If yes, then return the path, else return None."""
        path, _ = QFileDialog.getOpenFileName(self, self.tr("Select KML File"), "", self.tr("KML Files (*.kml *.kmz)"))
        if path and Path(path).exists() and Path(path).is_file():
            return Path(path)
        return None

    def open_kml_file(self, path: Path):
        """loads and displays a given kml/kmz file."""
        def progress_callback(message):
            """show a message above the progressbar"""
            if message != "":
                pbarui.message.setText(message)

        def finished():
            self.logger.info("loading thread finished")
            self.setCursor(Qt.CursorShape.ArrowCursor)
            self.load_map()
            pbar.close()
        
        self.logger.debug("open_kml_file triggered")
        self.logger.info(f"starting loading of kml... (path: {path})")
        # reset the map to erase any previous data
        self.reset_map()
        # clear the view to draw attention to the progress dialog
        self.ui.webEngineView.setUrl("about:blank")
        # init the dialog
        pbarui = Ui_progressDialog()
        pbar = QDialog(self)
        pbarui.setupUi(pbar)
        # show busy indicator
        pbarui.progressBar.setRange(0, 0)
        pbar.show()
        # load kml in seperate thread to not block event loop
        worker = Worker(self.map.load_placemarks, path)
        worker.signals.progress.connect(progress_callback)
        worker.signals.finished.connect(finished)

        self.setCursor(Qt.CursorShape.WaitCursor)
        self.threadpool.start(worker)

    def clicked_in_map(self, data: str):
        self.logger.debug(f"data: |{data}|")
        self.ui.statusbar.showMessage(f"clicked on: {data}", 5000)
        self.spreadsheet.toggle_region(data)
            
        if self.ui.actionHighlighting_Test.isChecked():
            self.map.map_bridge.highlight_region(data)

    def openExcelFile(self, path: None):
        """opens excel with either the given path, or first prompts user for a path."""
        # if a path has been passed, that means it was called from the re-init signal, so do that
        if path:
            # just double check the spreadsheet is gone
            with contextlib.suppress(Exception):
                self.spreadsheet.__del__()
            self.spreadsheet = Spreadsheet(path, self)
            self.spreadsheet.re_init.connect(lambda: self.openExcelFile(self.spreadsheet.file_path))
            return
        
        path = Path(QFileDialog.getOpenFileName(self, self.tr("Open Excel File"), "", self.tr("Excel Files (*.xlsx *.xls)"))[0])
        if path.exists() and path.is_file():
            self.logger.info(f"opening excel file: {path}")
            if self.spreadsheet:
                # close the old spreadsheet if it exists
                self.spreadsheet.__del__()  
            self.spreadsheet = Spreadsheet(path, self)
            # enable the workbook settings action since we now have an open workbook to configure
            self.ui.actionWorkbook_Settings.setEnabled(True)
            self.spreadsheet.re_init.connect(lambda: self.openExcelFile(self.spreadsheet.file_path))
            
    def reset_map(self):
        """resets the map and re-establishes the webchannel"""
        self.map = Map(51.165691, 10.451526, 6, Path(self.tempdir.path()))
        self.ui.webEngineView.page().setWebChannel(self.map.webchannel)
        self.map.map_bridge.region_clicked_signal.connect(self.clicked_in_map)
            
    def show_about_dialog(self):
        dialog = QDialog(self)
        ui = Ui_aboutDialog()
        ui.setupUi(dialog)
        ui.versionLabel.setText(f"Version: {VERSION}")
        ui.commitLabel.setText(f"Commit: {get_commit()}")
        dialog.show()
        
    def display_error(self, error: str):
        """displays an error message in the webview"""
        html = """<div style="width:90%;height:200px;position:absolute;top:50%;left:50%;margin-left:-45%;margin-top:-100px;background-color:rgb(243,139,168);border-radius:16px">
            <h1 style="text-align: center;">{}</h1>
            <p style="text-align: center;"><strong>{}</strong></p>
            </div>"""
        html = html.format(self.tr("Uh Oh! Something went wrong!"), self.tr("Error: {}").format(error))
        self.ui.webEngineView.setHtml(html)
        
    def show_settings_dialog(self, settings: dict | None = None):
        """shows the settings dialog. if a dictionary with values is given, it fills those in."""
        # declare this early because it's needed in validate_kml_path()
        tempmap = None
        def validate_kml_path():
            # if saving is enabled, a path is provided and that path points to a valid file, accept the dialog
            if ui.saveMapLocationCheckBox.isChecked() and (Path(ui.mapLocationLineEdit.text()).exists() and Path(ui.mapLocationLineEdit.text()).is_file()):
                dialog.accept()
            # if the map is not supposed to be saved, prompt the user to select a temporary file
            elif not ui.saveMapLocationCheckBox.isChecked():
                # pull in variable from outside scope
                nonlocal tempmap
                tempmap = self.select_kml_file()
                self.logger.debug(f"selected temp map: {tempmap}")
                if not tempmap:
                    QMessageBox.critical(self, self.tr("Missing Map Location"), self.tr("Please select a valid map to open."))
                    # restart to let user select again
                    validate_kml_path()
                    return
                dialog.accept()
            else:
                QMessageBox.critical(self, self.tr("Missing Map Location"), self.tr("Please select a valid map using the 'Select File...' Button."))
                
        self.logger.debug("showing settings dialog")
        dialog = QDialog(self)
        ui = Ui_settingsDialog()
        ui.setupUi(dialog)
        # check if dictionary is provided, if yes then fill in the gui
        if settings:
            self.logger.debug("opened with settings dict, filling in gui")
            self.logger.debug(f"settings: {settings}")
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
        # show path in ui after selection
        ui.mapLocationButton.clicked.connect(lambda: ui.mapLocationLineEdit.setText(str(self.select_kml_file())))
        # show the dialog. if it was accepted, return the settings
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
                "temp_map": tempmap
            }
            self.logger.debug(f"settings: {new_settings}")
            # if a dict was provided, load config directly into spreadsheet if it exists
            if settings and self.spreadsheet: 
                self.spreadsheet.load_config(new_settings)
            return new_settings
        # just return the unchanged settings back
        if settings:
            return {
                "region_sheet": settings["region_sheet"].get_value(),
                "region_map_name_column": settings["region_map_name_column"].get_value(),
                "region_sheet_start_row": settings["region_sheet_start_row"].get_value(),
                "region_name_column": settings["region_name_column"].get_value(),
                "calc_sheet": settings["calc_sheet"].get_value(),
                "calc_column": settings["calc_column"].get_value(),
                "calc_range": settings["calc_range"].get_value(),
                "save_map_path": settings["save_map_path"].get_value(),
                "linked_map": settings["linked_map"].get_value(),
                "temp_map": settings["temp_map"].get_value(),
            }
        # if no settings were provided, this dialog was shown for initialisation, so reopen it and return it's result
        return self.show_settings_dialog()
