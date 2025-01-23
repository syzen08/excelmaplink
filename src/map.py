import time
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
    
    def load_placemarks(self, kml_path, progress_callback = None):
        if progress_callback:
            progress_callback.emit(0)
        self.kml_reader.loadKML(kml_path, progress_callback)
        print("getting points...")
        points = self.kml_reader.getPoints()
        if progress_callback:
            progress_callback.emit(50)
        print(f"adding {len(points)} points...")
        for i, point in enumerate(points):
            folium.Marker(location=[point[0], point[1]], tooltip=point[2], popup=point[3]).add_to(self.map)
            if progress_callback:
                progress_callback.emit(50 + int((i + 1) / len(self.kml_reader.placemarks) * 50))
        
        print("getting polygons...")
        polygons = self.kml_reader.getPolygons()
        print(f"adding {len(polygons)} polygons...")
        for i, polygon in enumerate(polygons):
            folium.Polygon(locations=polygon[0], color="red", fill_color="red", weight=1, tooltip=polygon[1], popup=polygon[2]).add_to(self.map)
            if i % 100 == 0:
                if progress_callback:
                    progress_callback.emit(50 + int(((i + 1) / len(self.kml_reader.placemarks) + len(points) / len(self.kml_reader.placemarks)) * 50))
        print("done")
        if progress_callback:
            progress_callback.emit(100)
        time.sleep(0.5) #wait for all signals to fire