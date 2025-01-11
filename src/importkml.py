from pathlib import Path

import kml2geojson.main as k2json


def convert_kml_to_geojson(kml_path: Path):
    geojson = k2json.convert(kml_path)
    return geojson[0]

if __name__ == "__main__":
    geojson = convert_kml_to_geojson(Path("./touren.kml"))
    print(geojson)