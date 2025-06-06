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
        # populate the currently calculated regions from the calc sheet
        self.get_currently_calculated_regions()
        
    
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
            
if __name__ == "__main__":
    spsh = Spreadsheet(Path("ÜBERSICHT DD - 3.0 05.04.2025 - sR (Ascheberg Touren ab Nienberge).xlsx"))