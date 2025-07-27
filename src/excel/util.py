from xlwings import Sheet

from src.excel.config import ConfigOption
from src.excel.region import Region


def range_string(column: str, start_row: int, end_row: int) -> str:
    '''returns a string in the format "A1:A10" for the given column and row range.'''
    
    return f"{column}{int(start_row)}:{column}{int(end_row)}"

def region_from_map_name(map_name: str, config: dict[ConfigOption], region_sheet: Sheet) -> Region:
    try:
        row = region_sheet[range_string(config["region_map_name_column"].get_value(), config["region_sheet_start_row"].get_value(), region_sheet.used_range.last_cell.row)].value.index(map_name) + config["region_sheet_start_row"].get_value()
    except ValueError:
        raise ValueError(f"region with map name {map_name} not found in region sheet {region_sheet.name}")
    
    excel_name = region_sheet[config["region_name_column"].get_value() + str(row)].value
    return Region(excel_name=excel_name, map_name=map_name, row=row)

def region_from_excel_name(excel_name: str, config: dict[ConfigOption], region_sheet: Sheet) -> Region:
    try:
        row = region_sheet[range_string(config["region_name_column"].get_value(), config["region_sheet_start_row"].get_value(), region_sheet.used_range.last_cell.row)].value.index(excel_name) + config["region_sheet_start_row"].get_value()
    except ValueError:
        raise ValueError(f"region with map name {excel_name} not found in region sheet {region_sheet.name}")
    
    map_name = region_sheet[config["region_map_name_column"].get_value() + str(row)].value
    return Region(excel_name=excel_name, map_name=map_name, row=row)