import json
import sys
import time
import traceback
from pathlib import Path

import kml2geojson.main as k2json
from PySide6.QtCore import QObject, QRunnable, Signal


class WorkerSignals(QObject):
    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)


def convert_kml_to_geojson(kml_path: Path, geojson_path: Path = None):
    print("converting...")
    time.sleep(0.1)
    geojson = k2json.convert(kml_path)
    print("done")
    if geojson_path is not None:
        with open(geojson_path, "w") as f:
            json.dump(geojson[0], f)
            return None
    return geojson

class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else: 
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()



if __name__ == "__main__":
    geojson = convert_kml_to_geojson(Path("./touren.kml"))
    print(geojson)