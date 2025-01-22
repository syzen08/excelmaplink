from pathlib import Path

import folium

from src.kml import KMLReader


class Map:
    def __init__(self, lat, lon, zoom, path: Path):
        self.lat = lat
        self.lon = lon
        self.zoom = zoom
        self.map = folium.Map(location=[lat, lon], zoom_start=zoom)
        self.kml_reader = KMLReader()
        if path.exists():
            self.path = path
        else:
            raise Exception("path does not exist")

    def save(self):
        self.map.save(str(Path(self.path / "map.html")))

    def get_html(self):
        return self.map.get_root().render()
    
    def load_placemarks(self, kml_path):
        self.kml_reader.loadKML(kml_path)
        points = self.kml_reader.getPoints()
        print(f"adding {len(points)} points...")
        for point in points:
            folium.Marker(location=[point[0], point[1]], tooltip=point[2], popup=point[3]).add_to(self.map)

        polygons = self.kml_reader.getPolygons()
        print(f"adding {len(polygons)} polygons...")
        for polygon in polygons:
            folium.Polygon(locations=polygon[0], color="red", fill_color="red", weight=1, tooltip=polygon[1], popup=polygon[2]).add_to(self.map)