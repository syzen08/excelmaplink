from pathlib import Path

from PySide6.QtCore import QUrl
from PySide6.QtQuickWidgets import QQuickWidget
from PySide6.QtWidgets import (
    QGridLayout,
    QMainWindow,
    QSpacerItem,
    QWidget,
)


class MainWindow(QMainWindow):
    def __init__(self, data_url):
        super().__init__()

        self.setMinimumSize(800, 600)

        mainlayout = QGridLayout()
        widget = QWidget()
        widget.setLayout(mainlayout)
        self.setCentralWidget(widget)

        # placeholder widgets
        self.spacerL = QSpacerItem(200, 0)
        mainlayout.addItem(self.spacerL, 0, 1)

        self.qtquick = QQuickWidget()
        self.qtquick.setResizeMode(QQuickWidget.SizeRootObjectToView)
        self.qtquick.rootContext().setContextProperty("dataPath", data_url)
        self.engine = self.qtquick.engine()
        self.qtquick.setSource(QUrl.fromLocalFile(str(Path("./ui/qml/main.qml"))))
        mainlayout.addWidget(self.qtquick, 0, 0)
        if not self.qtquick.rootObject():
            raise Exception("Failed to load QML")
