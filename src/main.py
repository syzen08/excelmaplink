import sys
import traceback
from pathlib import Path

from PySide6.QtCore import QUrl
from PySide6.QtQuickWidgets import QQuickWidget
from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QMainWindow,
    QMessageBox,
    QSpacerItem,
    QWidget,
)


class MainWindow(QMainWindow):
    def __init__(self):
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
        self.qtquick.setSource(QUrl.fromLocalFile(str(Path("./ui/qml/main.qml"))))
        mainlayout.addWidget(self.qtquick, 0, 0)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Unexpected error:", e)
        print(traceback.format_exc())
        errmsgbox = QMessageBox()
        errmsgbox.setText(f"Unexpected error: {e}")
        errmsgbox.setDetailedText(traceback.format_exc())
        errmsgbox.setIcon(QMessageBox.Icon.Critical)
        errmsgbox.exec()
        sys.exit(1)

