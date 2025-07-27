from pathlib import Path

import xlwings as xw
from PySide6.QtCore import QLoggingCategory, Signal, qCDebug, qCInfo, qCWarning


class Spreadsheet:
    show_init_dialog = Signal()
    
    def __init__(self, file_path: Path, main_window):
        self.log_category = QLoggingCategory("excel")
        self.file_path = file_path
        self.main_window = main_window
        if not self.file_path.exists():
            raise FileNotFoundError(f"The file {self.file_path} does not exist.")
        # check if excel is running, if yes then connect to to it, otherwise start a new instance
        if xw.apps.active is not None:
            qCDebug(self.log_category, "excel is already running, using it")
            self.created = False
            self.app = xw.apps.active
            self.wb = self.app.books.open(str(self.file_path)) # BUG: this errors out if excel is already open with the file
        else:
            qCDebug(self.log_category, "excel isn't running, starting it...")
            self.created = True
            self.wb = xw.Book(str(self.file_path))
            self.app = self.wb.app
        qCDebug(self.log_category, f"spreadsheet: {self.wb.name}, sheets: {self.wb.sheets}")
        settings = self.get_config_options()
        
        # TODO: autocalc column
        self.config = {
            "region_sheet": ConfigOption(self.config_sheet, "region_sheet", "A"),
            "region_map_name_column": ConfigOption(self.config_sheet, "region_map_name_column", "B"),
            "region_sheet_start_row": ConfigOption(self.config_sheet, "region_map_name_start_row", "C"),
            "region_name_column": ConfigOption(self.config_sheet, "region_name_column", "D"),
            "calc_sheet": ConfigOption(self.config_sheet, "calc_sheet", "E"),
            "calc_column": ConfigOption(self.config_sheet, "calc_column", "F"),
            "calc_range": ConfigOption(self.config_sheet, "calc_range", "G"),
            "save_map_path": ConfigOption(self.config_sheet, "save_map_path", "H"),
            "linked_map": ConfigOption(self.config_sheet, "linked_map", "I"),
            "temp_map": ConfigOption(self.config_sheet, "temp_map", "J")
        }
        
        if settings:
            for key, value in settings.items():
                if key in self.config:
                    self.config[key].set_value(value)
                else:
                    qCWarning(self.log_category, f"unknown config option {key}, ignoring.")
        
        self.region_sheet = self.wb.sheets[self.config["region_sheet"].get_value()]
        self.calc_sheet = self.wb.sheets[self.config["calc_sheet"].get_value()]
        self.region_map_name_column = self.config["region_map_name_column"].get_value()
        self.region_map_name_start_row = self.config["region_sheet_start_row"].get_value()
        self.region_name_column = self.config["region_name_column"].get_value()
        self.calc_column = self.config["calc_column"].get_value()
        self.calc_range = self.config["calc_range"].get_value().split("@@")
        self.save_map_path = self.config["save_map_path"].get_value()
        self.linked_map = self.config["linked_map"].get_value()
        self.temp_map = self.config["temp_map"].get_value()
        self.cur_calcd_regions = []
        
        # populate the currently calculated regions from the calc sheet
        self.get_currently_calculated_regions()
        
        if self.save_map_path:
            qCInfo(self.log_category, f"loading linked map {self.linked_map}")
            self.main_window.open_kml_file(Path(self.linked_map))
        else:
            qCWarning(self.log_category, "implement")
            raise NotImplementedError("too lazy to implement this right now")
        
        
    
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
            
    def get_currently_calculated_regions(self):
        '''reads the currently calculated regions from the calc sheet and stores them in self.cur_calcd_regions.'''
        self.cur_calcd_regions = self.calc_sheet[self.range_string(self.calc_column, self.calc_range[0], self.calc_range[1])].value
        qCInfo(self.log_category, f"currently calculated regions: {self.cur_calcd_regions}")
        
    def range_string(self, column: str, start_row: int, end_row: int = -1) -> str:
        '''returns a string in the format "A1:A10" for the given column and row range.
        if end_row is -1, it will use the last row of the used range in the sheet.'''
        
        if end_row == -1:
            end_row = self.region_sheet.used_range.last_cell.row
        return f"{column}{start_row}:{column}{end_row}"

    def toggle_region(self, region_name: str):
        '''toggles the given region in the spreadsheet, adding if its not there and removing if it is.'''
        
        # this code is absolute shit, copilot did a lot of the heavy lifting here. i should eventually rewrite it so it's actually humanly comprehensible and not repeating all the time
        # but it finally fucking works
        # TODO: this is weird, make it not
        
        # check if the region exists in the spreadsheet
        try:
            row = self.region_sheet[self.range_string(self.region_map_name_column, self.region_map_name_start_row)].value.index(region_name)
        except ValueError:
            # try again but with underscores instead of spaces
            try:
                row = self.region_sheet[self.range_string(self.region_map_name_column, self.region_map_name_start_row)].value.index(region_name.replace(" ", "_"))
            except ValueError:
                # somethings probably wrong here, let's not risk breaking the spreadsheet
                raise ValueError(f"region name {region_name} not found in the map name column.")
        
        # convert the map name to the proper name
        region_name = self.region_sheet[self.region_name_column + str(self.region_map_name_start_row + row)].value
        # if the region is already in the calc range, remove it
        if region_name in self.cur_calcd_regions:
            qCInfo(self.log_category, f"removing {region_name} from currently calculated regions")
            self.cur_calcd_regions[self.cur_calcd_regions.index(region_name)] = None
        # otherwise add it
        else: 
            qCInfo(self.log_category, f"adding {region_name} to currently calculated regions")
            self.cur_calcd_regions[self.cur_calcd_regions.index(None)] = region_name
            
        # write the updated list back to the spreadsheet
        qCDebug(self.log_category, f"setting {self.range_string(self.calc_column, self.calc_range[0], self.calc_range[1])} to {self.cur_calcd_regions}")
        self.calc_sheet.range(self.range_string(self.calc_column, self.calc_range[0], self.calc_range[1])).options(transpose=True).value = self.cur_calcd_regions #using the transpose to write in row orientation
            
    def get_config_options(self):
        if "excelmaplink_config" not in [sheet.name for sheet in self.wb.sheets]:
            qCInfo(self.log_category, "no config sheet found")
            self.wb.sheets.add("excelmaplink_config")
            self.config_sheet: xw.Sheet = self.wb.sheets["excelmaplink_config"]
            # self.config_sheet.visible = False
            settings = self.main_window.show_settings_dialog()
            return settings
        else:
            qCInfo(self.log_category, "config sheet found")
            self.config_sheet: xw.Sheet = self.wb.sheets["excelmaplink_config"]
            return None
            
class ConfigOption:
    def __init__(self, sheet: xw.Sheet, name: str, column: str, value: str = ""):
        self.sheet = sheet
        self.name = name
        self.column = column
        
        # if the name is not set, then the sheet is either not initialized or out of date, so reset it
        # ?: find a way to migrate old options
        if not self.sheet[self.column + "1"].value == self.name:
            self.sheet[self.column + "1"].value = self.name
            self.sheet[self.column + "2"].value = value
            qCDebug(QLoggingCategory("excel"), f"reset config option {self.name}")
        
    def get_value(self) -> str:
        """returns the value of the config option."""
        val = self.sheet[self.column + "2"].value
        if val == "NONE":
            return None
        return val
    
    def set_value(self, value: str):
        """sets the value of the config option."""
        qCInfo(QLoggingCategory("excel"), f"set config option {self.name} to {value}")
        if value is None:
            value = "NONE"
        if isinstance(value, tuple):
            value = "@@".join(map(str, value))
        self.sheet[self.column + "2"].value = value
        
        
if __name__ == "__main__":
    spsh = Spreadsheet(Path("ÜBERSICHT DD - 3.0 05.04.2025 - sR (Ascheberg Touren ab Nienberge).xlsx"))