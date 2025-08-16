import logging
from typing import Any

from xlwings import Sheet


class ConfigOption:
    def __init__(self, sheet: Sheet, name: str, column: str, type: str):
        """initialises a single config option.
        - `sheet` is a reference to the excel sheet to write to
        - `column` is the column to write into
        - `type` signals what type the value is. possible values are:
          - `"s"` = string
          - `"i"` = integer
          - `"b"` = boolean
          - `"t"` = tuple"""
        self.sheet = sheet
        self.name = name
        self.column = column
        self.logger = logging.getLogger("eml.spreadsheet.config")
        if len(type) > 1:
            raise ValueError("type must be a single character. got: " + type)
        if type not in ["s", "i", "b", "t"]:
            raise ValueError("type must be one of 's' (string), 'i' (int), 'b' (bool), 't' (tuple)). got: " + type)
        self.type = type
        
        # if the name is not set, then the sheet is either not initialized or out of date, so reset it
        # ?: find a way to migrate old options
        if not self.sheet[self.column + "1"].value == self.name:
            self.sheet[self.column + "1"].value = self.name
            self.sheet[self.column + "2"].value = ""
            self.logger.debug(f"reset config option {self.name}")
            
    def __repr__(self):
        return f"ConfigOption(name: {self.name}, type: {self.type}, column: {self.column}, value: {self.get_value()})"
    
    def __str__(self) -> str:
        return str(self.get_value())
            
    def convert_to_type(self):
        match self.type:
            case "s":
                return str(self.sheet[self.column + "2"].value)
            case "i":
                return int(self.sheet[self.column + "2"].value)
            case "b":
                # xlwings already handles this
                return self.sheet[self.column + "2"].value
            case "t":
                return tuple(map(int, self.sheet[self.column + "2"].value.split("@@")))
            case _:
                raise ValueError(f"unknown type {self.type}, how did you even get here?")
        
    def get_value(self) -> str | int | bool | tuple:
        """returns the value of the config option."""
        val = self.sheet[self.column + "2"].value
        if val == "NONE":
            return None
        return self.convert_to_type()
    
    def set_value(self, value: Any):
        """sets the value of the config option."""
        self.logger.info(f"set config option {self.name} to {value}")
        if value is None or value in ["None", "none", "NONE"]:
            value = "NONE"
        if isinstance(value, tuple):
            value = "@@".join(map(str, value))
        self.sheet[self.column + "2"].value = str(value)
        