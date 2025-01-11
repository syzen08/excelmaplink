import json
import sys
import traceback
from pathlib import Path

from PySide6.QtCore import QTemporaryDir, QUrl
from PySide6.QtWidgets import QApplication, QMessageBox

from src import importkml
from ui.mainwindow import MainWindow


def main():
    app = QApplication(sys.argv)
    kml_path = Path("./touren.kml")
    temp_dir = QTemporaryDir()
    if (temp_dir.isValid()):
        geojson_path = Path(temp_dir.path() + "/touren.geojson")
        geojson = importkml.convert_kml_to_geojson(kml_path)
        with open(geojson_path, "w") as f:
            json.dump(geojson, f)
    else:
        raise Exception("Failed to create temporary directory")
    url = QUrl.fromLocalFile(str(geojson_path))
    print(url.url())
    window = MainWindow(url)
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

