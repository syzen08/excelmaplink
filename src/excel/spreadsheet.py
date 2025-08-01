from pathlib import Path

import xlwings as xw
from PySide6.QtCore import (
    QCoreApplication,
    QLoggingCategory,
    qCCritical,
    qCDebug,
    qCInfo,
    qCWarning,
)
from PySide6.QtWidgets import QMessageBox
from pywintypes import com_error

from src.excel.config import ConfigOption
from src.excel.cur_regions import CurrentRegions
from src.excel.util import range_string, region_from_excel_name


class Spreadsheet:
    def __init__(self, path: Path, main_window):
        self.log_category = QLoggingCategory("spreadsheet")
        self.file_path = path
        self.main_window = main_window
        if not self.file_path.exists():
            raise FileNotFoundError(f"file {self.file_path} does not exist. how do you want me to load that!?")

        #check if excel is already runnding
        if xw.apps.active is not None:
            #if yes, then connect to it
            qCDebug(self.log_category, "excel is already running, connecting to it...")
            self.app = xw.apps.active
            self.wb = self.app.books.open(str(self.file_path)) # BUG: this errors out if excel is already open with the file
        else:
            #if no, then start a new instance
            qCDebug(self.log_category, "excel isn't running, starting it...")
            self.created = True
            self.wb = xw.Book(str(self.file_path))
            self.app = self.wb.app
        qCDebug(self.log_category, f"spreadsheet: {self.wb.name}, sheets: {self.wb.sheets}")
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

        if settings:
            self.import_settings(settings)
            self.populate_cur_regions()
            self.load_map()

    def __del__(self):
        """close the workbook and quit the app when the object is deleted."""
        # if we created the app, we close it, otherwise we just leave it open
        if self.created:
            qCDebug(self.log_category, "closing workbook and quitting app...")
        else:
            qCDebug(self.log_category, "excel was not created by me, not closing.")
        if self.wb and self.created:
            self.wb.close()
        if self.app and self.created:
            self.app.quit()

    def toggle_region(self, region_map_name: str):
        try:
            self.cur_calc_regions.toggle_region(region_map_name)
        except ValueError as e:
            qCCritical(self.log_category, f"could not toggle region {region_map_name}: {e}")
            QMessageBox.critical(self.main_window, QCoreApplication.translate("Spreadsheet", "Region Not Found"), QCoreApplication.translate("Spreadsheet", "Could not find region {} in region sheet {}.\nPlease make sure that you have the correct column selected in the settings and the names in the column are the correct format.").format(region_map_name, self.region_sheet.name))
        qCDebug(self.log_category, f"cur_regions: {self.cur_calc_regions.regions}")
        
        self.calc_sheet.range(range_string(self.config["calc_column"].get_value(), *self.config["calc_range"].get_value())).options(transpose=True).value = [r.excel_name if r is not None else None for r in self.cur_calc_regions.regions]

    def get_config_options(self):
        if "excelmaplink_config" not in [sheet.name for sheet in self.wb.sheets]:
            qCInfo(self.log_category, "no config sheet found, creating one...")
            self.wb.sheets.add("excelmaplink_config")
            self.config_sheet: xw.Sheet = self.wb.sheets["excelmaplink_config"]
            # self.config_sheet.visible = False
            settings = self.main_window.show_settings_dialog()
            return settings
        else:
            qCInfo(self.log_category, "config sheet found, loading settings...")
            self.config_sheet: xw.Sheet = self.wb.sheets["excelmaplink_config"]
            return None
        
    def import_settings(self, settings: dict):
        """import settings from a dictionary."""
        for key, value in settings.items():
            if key in self.config:
                self.config[key].set_value(value)
            else:
                qCWarning(self.log_category, f"unknown config option {key}, ignoring.")
        try:
            self.region_sheet = self.wb.sheets[self.config["region_sheet"].get_value()]
            self.calc_sheet = self.wb.sheets[self.config["calc_sheet"].get_value()]
        except com_error as e:
            qCCritical(self.log_category, f"could not find sheet {self.config['region_sheet'].get_value()} or {self.config['calc_sheet'].get_value()}: {e}")
            QMessageBox.critical(self.main_window, QCoreApplication.translate("Spreadsheet", "Sheet Not Found"), QCoreApplication.translate("Spreadsheet", "Could not find sheet {} or {}. Please check your settings.").format(self.config['region_sheet'].get_value(), self.config['calc_sheet'].get_value()))
            settings = self.main_window.show_settings_dialog(self.config)
            if settings:
                self.import_settings(settings)
            return
        qCDebug(self.log_category, "settings imported successfully")
        
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
                qCWarning(self.log_category, f"could not find region {cell} in region sheet {self.region_sheet.name}: {e}")
                cur_regions.append(None)
        self.cur_calc_regions = CurrentRegions(cur_regions, self.config["calc_range"].get_value()[1] - self.config["calc_range"].get_value()[0] + 1, self.main_window)
        qCDebug(self.log_category, f"current calc regions: {self.cur_calc_regions.regions}")
        
    def load_map(self):
        if self.config["save_map_path"].get_value():
            qCInfo(self.log_category, f"loading map from {self.config['linked_map'].get_value()}")
            self.main_window.open_kml_file(Path(self.config["linked_map"].get_value()))
        else:
            raise NotImplementedError("TODO: implement loading of temp map")
        
    def load_config(self, settings: dict):
        if settings:
            self.import_settings(settings)
        self.populate_cur_regions()
        self.load_map()