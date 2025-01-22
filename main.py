import sys
import traceback

from PySide6.QtWidgets import QApplication, QMessageBox

from ui.mainwindow import MainWindow


def main():
    app = QApplication(sys.argv)

    window = MainWindow(None)
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

