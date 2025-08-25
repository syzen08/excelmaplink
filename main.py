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
    qFormatLogMessage,
    qInstallMessageHandler,
    qSetMessagePattern,
)
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMessageBox
from rich.console import Console
from rich.logging import RichHandler
from rich.traceback import Traceback

import resources_rc  # noqa: F401
from src.mainwindow import MainWindow
from src.version.version import VERSION

#configue splash screen in frozen builds
if getattr(sys, "frozen", False):
    import pyi_splash  # pyright: ignore[reportMissingModuleSource]

# set taskbar icon
try:
    from ctypes import windll
    appid = f"com.syzen.excelmaplink.{VERSION}"
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(appid)
except ImportError:
    pass

def main(logger: logging.Logger):
    parser = argparse.ArgumentParser(prog=f"excelmaplink v{VERSION}")
    parser.add_argument("--debug", action="store_true")
    debug_mode = parser.parse_args().debug
    if debug_mode:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.WARNING)
    
    QLoggingCategory.setFilterRules("""*.info=true
                                    qt.widgets.painting.info=false""")
    
    app = QApplication(sys.argv)
    
    path = QLibraryInfo.path(QLibraryInfo.TranslationsPath)
    translator = QTranslator(app)
    if translator.load(QLocale.system(), "qtbase", "_", path):
        app.installTranslator(translator)
    translator = QTranslator(app)
    path = ":/translations"
    if translator.load(QLocale.system(), "app", "_", path):
        app.installTranslator(translator)
        
    QApplication.setStyle("Fusion")
    app.setWindowIcon(QIcon(":/icons/icon.ico"))
    logger.info(f"--- excelmaplink version {VERSION} ---")
    logger.debug("init mainwindow")
    window = MainWindow(debug_mode)
    if getattr(sys, "frozen", False):   
        pyi_splash.close()
    window.show()
    sys.exit(app.exec())
    
def qt_message_handler(mode, context, message):
    formatted_message = qFormatLogMessage(mode, context, message)
    match mode:
        case QtMsgType.QtDebugMsg:
            qtlogger.debug(formatted_message)
        case QtMsgType.QtInfoMsg:
            qtlogger.info(formatted_message)
        case QtMsgType.QtWarningMsg:
            qtlogger.warning(formatted_message)
        case QtMsgType.QtCriticalMsg:
            qtlogger.error(formatted_message)
        case QtMsgType.QtFatalMsg:
            qtlogger.critical(formatted_message)

def global_exception_hook(exctype, value, tb):
    # ngl completely over the top and unnecessary but fun.
    
    # print rich traceback
    console = Console(stderr=True)
    rich_tb = Traceback.from_exception(exctype, value, tb, show_locals=True)
    console.print(rich_tb)
    
    errmsgbox = QMessageBox()
    errmsgbox.setIcon(QMessageBox.Icon.Critical)
    errmsgbox.setWindowTitle(QApplication.translate("MainWindow", "Unexpected error"))
    errmsgbox.setText(QApplication.translate("MainWindow", "An unexpected error occurred."))
    errmsgbox.setInformativeText(f"{exctype.__name__}: {value}")
    errmsgbox.setDetailedText("".join(traceback.format_tb(tb)))
    continue_button = errmsgbox.addButton(QApplication.translate("MainWindow", "Continue"), QMessageBox.ButtonRole.AcceptRole)
    quit_button = errmsgbox.addButton(QApplication.translate("MainWindow", "Quit"), QMessageBox.ButtonRole.RejectRole)
    errmsgbox.setDefaultButton(quit_button)
    errmsgbox.exec()
    if errmsgbox.clickedButton() == continue_button:
        btn = QMessageBox.question(
            None, 
            QApplication.translate("MainWindow", "WARNING!"), 
            QApplication.translate("MainWindow", "This will continue execution in this unknown state. This can lead to unexpected behaviour. Do you really want to continue?")
        )
        if btn == QMessageBox.StandardButton.Yes:
            return
    sys.exit(-1)
    
if __name__ == "__main__":
    freeze_support()
    if getattr(sys, "frozen", False):   
        pyi_splash.update_text("Loading UI...")
    sys.excepthook = global_exception_hook
    logging.basicConfig(
        level="NOTSET", format="[%(name)s]: %(message)s", datefmt="[%X]", handlers=[RichHandler(rich_tracebacks=True)]
    )
    logger = logging.getLogger("eml")
    qtlogger = logging.getLogger("eml.qt")
    qSetMessagePattern("<%{category}>: %{message}")
    qInstallMessageHandler(qt_message_handler)
    
    main(logger)
