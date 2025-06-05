from pathlib import Path

import xlwings as xw
from PySide6.QtCore import QLoggingCategory, qCDebug, qCInfo


class Spreadsheet:
    def __init__(self, file_path: Path, region_sheet: str, region_map_name_column: str, region_map_name_start_row: int, region_name_column: str, calc_sheet: str, calc_column: str, calc_range: tuple[int, int]):
        self.log_category = QLoggingCategory("excel")
        self.file_path = file_path
        self.region_sheet = region_sheet
        self.region_map_name_column = region_map_name_column
        self.region_map_name_start_row = region_map_name_start_row
        self.region_name_column = region_name_column
        self.calc_sheet = calc_sheet
        self.calc_column = calc_column
        self.calc_range = calc_range
        self.cur_calcd_regions = []
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
        self.region_sheet = self.wb.sheets[self.region_sheet]
        self.calc_sheet = self.wb.sheets[self.calc_sheet]
        self.get_currently_calculated_regions()
        
    
    def __del__(self):
        """close the workbook and quit the app when the object is deleted."""
        if self.created:
            qCDebug(self.log_category, "closing workbook and quitting app...")
        else:
            qCDebug(self.log_category, "excel was not created by me, not closing.")
        if self.wb and self.created:
            self.wb.close()
        if self.app and self.created:
            self.app.quit()
            
    def get_currently_calculated_regions(self):
        self.cur_calcd_regions = self.calc_sheet[self.calc_column + str(self.calc_range[0]) + ":" + self.calc_column + str(self.calc_range[1])].value
        qCInfo(self.log_category, f"currently calculated regions: {self.cur_calcd_regions}")
        
        
    def toggle_region(self, region_name: str):

        # this code is absolute shit, copilot did a lot of the heavy lifting here. i should eventually rewrite it so it's actually humanly comprehensible and not repeating all the time
        # but it finally fucking works
        try:
            row = self.region_sheet[self.region_map_name_column + str(self.region_map_name_start_row) + ":" + self.region_map_name_column + str(self.region_sheet.used_range.last_cell.row)].value.index(region_name)
        except ValueError:
            try:
                row = self.region_sheet[self.region_map_name_column + str(self.region_map_name_start_row) + ":" + self.region_map_name_column + str(self.region_sheet.used_range.last_cell.row)].value.index(region_name.replace(" ", "_"))
            except ValueError:
                raise ValueError(f"region name {region_name} not found in the map name column.")
            
        region_name = self.region_sheet[self.region_name_column + str(self.region_map_name_start_row + row)].value
        if region_name in self.cur_calcd_regions:
            qCInfo(self.log_category, f"removing {region_name} from currently calculated regions")
            self.cur_calcd_regions[self.cur_calcd_regions.index(region_name)] = None
        else: 
            qCInfo(self.log_category, f"adding {region_name} to currently calculated regions")
            self.cur_calcd_regions[self.cur_calcd_regions.index(None)] = region_name
            
        qCDebug(self.log_category, f"setting {self.calc_column + str(self.calc_range[0]) + ':' + self.calc_column + str(self.calc_range[1])} to {self.cur_calcd_regions}")
        self.calc_sheet.range(self.calc_column + str(self.calc_range[0]) + ":" + self.calc_column + str(self.calc_range[1])).options(transpose=True).value = self.cur_calcd_regions
            
if __name__ == "__main__":
    spsh = Spreadsheet(Path("ÜBERSICHT DD - 3.0 05.04.2025 - sR (Ascheberg Touren ab Nienberge).xlsx"))