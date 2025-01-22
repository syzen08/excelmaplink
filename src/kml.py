from fastkml import Placemark, kml
from fastkml.utils import find_all
from pygeoif.geometry import MultiPolygon, Point, Polygon


class KMLReader:
    def __init__(self, kml_path=None):
        self.kml_path = kml_path
        self.kml = None

    def loadKML(self, kml_path=None):
        if kml_path is not None:
            self.kml_path = kml_path
        
        if self.kml_path is None:
            raise Exception("No KML file specified")
        
        self.kml = kml.KML.parse(self.kml_path)
        self.placemarks = list(find_all(self.kml, of_type=Placemark))
        print(f"loaded {len(self.placemarks)} placemarks")

    def getPoints(self):
        points = []
        for placemark in self.placemarks:
            point = placemark.geometry
            if isinstance(point, Point):
                points.append((point.coords[0][1], point.coords[0][0], placemark.name, placemark.description))
        print(len(points))
        return points

    def getPolygons(self):
        polygons = []
        for placemark in self.placemarks:
            polygon = placemark.geometry
            if isinstance(polygon, MultiPolygon):
                for poly in polygon.geoms:
                    points = []
                    for point in poly.exterior.coords:
                        points.append((point[1], point[0]))
                    polygons.append((points, placemark.name, placemark.description))
            if isinstance(polygon, Polygon):
                points = []
                for point in polygon.exterior.coords:
                    points.append((point[1], point[0]))
                polygons.append(points)
        return polygons
