import sys
from pathlib import Path

from PySide6.QtCore import QCoreApplication, QLoggingCategory, QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuickControls2 import QQuickStyle

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    QLoggingCategory.setFilterRules("*.info=true")
    QQuickStyle.setStyle("FluentWinUI3")
    engine = QQmlApplicationEngine()
    engine.addImportPath(Path(__file__).parent)
    engine.rootContext().setContextProperty("dataPath", QUrl.fromLocalFile(str(Path("./data/default.geojson").absolute())))
    engine.loadFromModule("ExcelMapLink", "Main")
    engine.quit.connect(QCoreApplication.quit)

    if not engine.rootObjects():
        raise Exception("failed to load")
    
    exit_code = app.exec()
    del engine
    sys.exit(exit_code)

