from pathlib import Path

import xlwings as xw
from PySide6.QtCore import QLoggingCategory, qCDebug, qCInfo


class Spreadsheet:
    def __init__(self, file_path: Path):
        self.log_category = QLoggingCategory("excel")
        self.file_path = file_path
        if not self.file_path.exists():
            raise FileNotFoundError(f"The file {self.file_path} does not exist.")
        # check if excel is running, if yes then connect to to it, otherwise start a new instance
        if xw.apps.active is not None:
            qCDebug(self.log_category, "excel is already running, using it")
            self.created = False
            self.app = xw.apps.active
            self.wb = self.app.books.open(str(self.file_path))
        else:
            qCDebug(self.log_category, "excel isn't running, starting it...")
            self.created = True
            self.wb = xw.Book(str(self.file_path))
            self.app = self.wb.app
        qCDebug(self.log_category, f"spreadsheet: {self.wb.name}, sheets: {self.wb.sheets}")
    
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
            
if __name__ == "__main__":
    spsh = Spreadsheet(Path("ÜBERSICHT DD - 3.0 05.04.2025 - sR (Ascheberg Touren ab Nienberge).xlsx"))