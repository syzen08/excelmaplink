import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication, QGridLayout, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())