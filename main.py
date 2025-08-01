import sys
import traceback

from PySide6.QtCore import (
    QLibraryInfo,
    QLocale,
    QLoggingCategory,
    QTranslator,
    qSetMessagePattern,
)
from PySide6.QtWidgets import QApplication, QMessageBox
from rich.traceback import install

import translations_rc
from src.mainwindow import MainWindow

# Guide: Also, wenn ich in der Karte eine mehrere Touren anklicke, soll er den Namen (aus C oder AP ) in den Reiter Berechnung in Spalte B  ab zeile 6 bis 24 auflisten ….

def main():
    install(show_locals=True)
    QLoggingCategory.setFilterRules("""*.info=true
                                    qt.widgets.painting.info=false""")
    qSetMessagePattern("[%{time process}] [%{if-debug}DEBUG%{endif}%{if-info}INFO%{endif}%{if-warning}WARN%{endif}%{if-critical}CRITICAL%{endif}%{if-fatal}FATAL%{endif}] <%{category}>: %{message}")
    app = QApplication(sys.argv)
    path = QLibraryInfo.location(QLibraryInfo.TranslationsPath)
    translator = QTranslator(app)
    if translator.load(QLocale.system(), 'qtbase', '_', path):
        app.installTranslator(translator)
    translator = QTranslator(app)
    path = ':/translations'
    if translator.load(QLocale.system(), 'app', '_', path):
        app.installTranslator(translator)
    QApplication.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Unexpected error:", e)
        print(traceback.format_exc())
        # show error message box on exception
        errmsgbox = QMessageBox()
        errmsgbox.setText(QApplication.translate("MainWindow", "Unexpected error: {}").format(e))
        errmsgbox.setDetailedText(traceback.format_exc())
        errmsgbox.setIcon(QMessageBox.Icon.Critical)
        errmsgbox.exec()
        sys.exit(1)

