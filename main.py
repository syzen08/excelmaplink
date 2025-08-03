import argparse
import logging
import sys
import traceback
from multiprocessing import freeze_support

from PySide6.QtCore import (
    QLibraryInfo,
    QLocale,
    QLoggingCategory,
    QtMsgType,
    QTranslator,
    qInstallMessageHandler,
)
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMessageBox
from rich.logging import RichHandler
from rich.traceback import install

import resources_rc  # noqa: F401
from src.mainwindow import MainWindow

# set taskbar icon
try:
    from ctypes import windll
    appid = "com.syzen.excelmaplink.1.0"
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(appid)
except ImportError:
    pass

# Guide: Also, wenn ich in der Karte eine mehrere Touren anklicke, soll er den Namen (aus C oder AP ) in den Reiter Berechnung in Spalte B  ab zeile 6 bis 24 auflisten ….

def main(logger: logging.Logger):

    parser = argparse.ArgumentParser(prog="excelmaplink")
    parser.add_argument('--debug', action='store_true')
    debug_mode = parser.parse_args().debug
    if debug_mode:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.WARNING)
    
    QLoggingCategory.setFilterRules("""*.info=true
                                    qt.widgets.painting.info=false""")
    
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
    app.setWindowIcon(QIcon(":/icons/icon.ico"))
    logger.debug("init mainwindow")
    window = MainWindow(debug_mode)
    window.show()
    sys.exit(app.exec())
    
def qt_message_handler(mode, context, message):
    match mode:
        case QtMsgType.QtDebugMsg:
            qtlogger.debug(message)
        case QtMsgType.QtInfoMsg:
            qtlogger.info(message)
        case QtMsgType.QtWarningMsg:
            qtlogger.warning(message)
        case QtMsgType.QtCriticalMsg:
            qtlogger.error(message)
        case QtMsgType.QtFatalMsg:
            qtlogger.critical(message)
            

if __name__ == "__main__":
    freeze_support()
    try:
        install(show_locals=True)
        logging.basicConfig(
            level="NOTSET", format="[%(name)s]: %(message)s", datefmt="[%X]", handlers=[RichHandler(rich_tracebacks=True)]
        )
        logger = logging.getLogger('eml')
        qtlogger = logging.getLogger('eml.qt')
        qInstallMessageHandler(qt_message_handler)
        
        main(logger)
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

