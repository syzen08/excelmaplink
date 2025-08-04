import logging
from pathlib import Path

import xlwings as xw
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QMessageBox
from pywintypes import com_error

from src.excel.config import ConfigOption
from src.excel.cur_regions import CurrentRegions
from src.excel.util import range_string, region_from_excel_name


class Spreadsheet(QObject):
    re_init = Signal()
    def __init__(self, path: Path, main_window):
        super().__init__()
        self.logger = logging.getLogger("eml.spreadsheet")
        self.file_path = path
        self.main_window = main_window
        if not self.file_path.exists():
            raise FileNotFoundError(f"file {self.file_path} does not exist. how do you want me to load that!?")

        self.start_excel()
        settings = self.get_config_options()

        self.config = {
            "region_sheet": ConfigOption(self.config_sheet, "region_sheet", "A", "s"),
            "region_map_name_column": ConfigOption(self.config_sheet, "region_map_name_column", "B", "s"),
            "region_sheet_start_row": ConfigOption(self.config_sheet, "region_map_name_start_row", "C", "i"),
            "region_name_column": ConfigOption(self.config_sheet, "region_name_column", "D", "s"),
            "calc_sheet": ConfigOption(self.config_sheet, "calc_sheet", "E", "s"),
            "calc_column": ConfigOption(self.config_sheet, "calc_column", "F", "s"),
            "calc_range": ConfigOption(self.config_sheet, "calc_range", "G", "t"),
            "save_map_path": ConfigOption(self.config_sheet, "save_map_path", "H", "b"),
            "linked_map": ConfigOption(self.config_sheet, "linked_map", "I", "s"),
            "temp_map": ConfigOption(self.config_sheet, "temp_map", "J", "s")
        }

        self.load_config(settings)
        # every 2.5 secs, try to reconnect to excel (implemented in timerEvent()) and re-init if excel closed out of our control
        self.timer_id = self.startTimer(2500)
        
        # update highlights once map has loaded
        self.main_window.map.map_bridge.finished_loading_signal.connect(self.cur_calc_regions.update_highligts)
        
    def __del__(self):
        """close the workbook and quit the app when the object is deleted."""
        # if we created the app, we close it, otherwise we just leave it open
        if self.created:
            # if this doesnt properly work, just ignore it, it's not that deep
            try:
                self.logger.debug("closing workbook and quitting app...")
            except Exception:
                pass
        else:
            try:
                self.logger.debug("excel was not created by me, not closing.")
            except Exception:
                pass
        if self.wb and self.created:
            self.wb.close()
        if self.app and self.created:
            self.app.quit()

    def timerEvent(self, event):
        self.logger.debug("checking excel...")
        try:
            # just something that requires access to excel
            val = self.app.range("A1:B1").value
            self.logger.debug(f"ok, still here. val {val}")
        except Exception:
            self.logger.error("lost connection to excel!")
            # stop the timer so this doesn't retrigger
            self.killTimer(self.timer_id)
            QMessageBox.warning(
                self.main_window, 
                self.tr("Lost connection to Excel"), 
                self.tr("Lost connection to Excel. Please DO NOT close Excel itself. Close the map instead, it will close Excel on its own.")
            )
            # tell the mainwindow to re-init the spreadsheet
            self.re_init.emit()
            

    def toggle_region(self, region_map_name: str):
        try:
            self.cur_calc_regions.toggle_region(region_map_name)
        except ValueError as e:
            self.logger.error(f"could not toggle region {region_map_name}: {e}")
            QMessageBox.critical(
                self.main_window, 
                self.tr("Region Not Found"), 
                self.tr("Could not find region {} in region sheet {}.\nPlease make sure that you have the correct column selected in the settings and the names in the column are the correct format.").format(region_map_name, self.region_sheet.name)
            )
        self.logger.debug(f"cur_regions: {self.cur_calc_regions.regions}")
        
        self.calc_sheet.range(range_string(self.config["calc_column"].get_value(), *self.config["calc_range"].get_value())).options(transpose=True).value = [r.excel_name if r is not None else None for r in self.cur_calc_regions.regions]

    def get_config_options(self):
        if "excelmaplink_config" not in [sheet.name for sheet in self.wb.sheets]:
            self.logger.info("no config sheet found, creating one...")
            self.wb.sheets.add("excelmaplink_config")
            self.config_sheet: xw.Sheet = self.wb.sheets["excelmaplink_config"]
            if not self.main_window.debug:
                self.config_sheet.visible = False
            settings = self.main_window.show_settings_dialog()
            return settings
        else:
            self.logger.info("config sheet found, loading settings...")
            self.config_sheet: xw.Sheet = self.wb.sheets["excelmaplink_config"]
            self.config_sheet.visible = self.main_window.debug
            return None
        
    def import_settings(self, settings: dict):
        """import settings from a dictionary."""
        for key, value in settings.items():
            if key in self.config:
                self.config[key].set_value(value)
            else:
                self.logger.warning(f"unknown config option {key}, ignoring.")
        self.logger.debug("settings imported successfully. saving...")
        self.wb.save()
        
    def get_sheets(self):
        try:
            self.region_sheet = self.wb.sheets[self.config["region_sheet"].get_value()]
            self.calc_sheet = self.wb.sheets[self.config["calc_sheet"].get_value()]
        except com_error as e:
            self.logger.error(f"could not find sheet {self.config['region_sheet'].get_value()} or {self.config['calc_sheet'].get_value()}: {e}")
            QMessageBox.critical(
                self.main_window, 
                self.tr("Sheet Not Found"), 
                self.tr("Could not find sheet {} or {}. Please check your settings.").format(self.config['region_sheet'].get_value(), self.config['calc_sheet'].get_value())
            )
            settings = self.main_window.show_settings_dialog(self.config)
            if settings:
                self.load_config(settings)
                return -1
        
    def populate_cur_regions(self):
        cur_regions = []
        for cell in self.calc_sheet.range(range_string(self.config["calc_column"].get_value(), *self.config["calc_range"].get_value())).value:
            if cell is None:
                cur_regions.append(None)
                continue
            try:
                region = region_from_excel_name(cell, self.config, self.region_sheet)
                cur_regions.append(region)
            except ValueError as e:
                self.logger.error(f"could not find region {cell} in region sheet {self.region_sheet.name}: {e}")
                cur_regions.append(None)
        self.cur_calc_regions = CurrentRegions(cur_regions, self.config["calc_range"].get_value()[1] - self.config["calc_range"].get_value()[0] + 1, self.main_window)
        self.logger.debug(f"current calc regions: {self.cur_calc_regions.regions}")
        
    def load_map(self):
        if self.config["save_map_path"].get_value():
            if not Path(self.config['linked_map'].get_value()).exists():
                self.logger.error("map does not exist at stored location!")
                self.main_window.display_error(self.tr("Spreadsheet", "The map at {} could not be found.").format(str(Path(self.config['linked_map'].get_value()))))
                QMessageBox.critical(
                    self.main_window, 
                    self.tr("Map not found"), 
                    self.tr("The map at {} could not be found. Make sure that the file path is still accessible and exists.").format(str(Path(self.config['linked_map'].get_value())))
                )
                #clear webview to signal to user that something is wrong
                return -1
            self.logger.info(f"loading map from {self.config['linked_map'].get_value()}")
            self.main_window.open_kml_file(Path(self.config["linked_map"].get_value()))
        elif self.config["temp_map"].get_value():
            self.logger.info(f"loading temp map from {self.config['temp_map'].get_value()}")
            self.main_window.open_kml_file(Path(self.config['temp_map'].get_value()))
            self.logger.info("wiping temp map config")
            self.config['temp_map'].set_value(None)
        else:
            self.logger.warning("no map location found!")
            new_settings = self.main_window.show_settings_dialog(self.config)
            self.load_config(new_settings)
        
    def load_config(self, settings: dict = None):
        if settings:
            self.import_settings(settings)
        if self.get_sheets() == -1:
            return
        self.populate_cur_regions()
        self.load_map()
        
    def start_excel(self):
        #check if excel is already runnding
        if xw.apps.active is not None:
            #if yes, then connect to it
            self.logger.debug("excel is already running, connecting to it...")
            self.app = xw.apps.active
            self.wb = self.app.books.open(str(self.file_path)) # BUG: this errors out if excel is already open with the file
        else:
            #if no, then start a new instance
            self.logger.debug("excel isn't running, starting it...")
            self.created = True
            self.wb = xw.Book(str(self.file_path))
            self.app = self.wb.app
        self.logger.debug(f"spreadsheet: {self.wb.name}, sheets: {self.wb.sheets}")