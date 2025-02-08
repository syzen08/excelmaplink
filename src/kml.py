from fastkml import Placemark, kml
from fastkml.styles import IconStyle, LineStyle, PolyStyle, StyleMap
from fastkml.utils import find_all
from pygeoif.geometry import MultiPolygon, Point, Polygon


class KMLReader:
    def __init__(self, kml_path=None):
        self.kml_path = kml_path
        self.kml = None

    def loadKML(self, kml_path=None, progress_callback = None):
        if kml_path is not None:
            self.kml_path = kml_path
        
        if self.kml_path is None:
            raise Exception("No KML file specified")
        
        print(f"loading {self.kml_path}...")
        if progress_callback:
            progress_callback.emit(0, f"loading {self.kml_path}...")
        self.kml = kml.KML.parse(self.kml_path)
        print("loading placemarks...")
        if progress_callback is not None:
            progress_callback.emit(20, "loading placemarks...")
        self.placemarks = list(find_all(self.kml, of_type=Placemark))
        print(f"loaded {len(self.placemarks)} placemarks")
        if progress_callback is not None:
            progress_callback.emit(40, "loading styles...")
        print("creating style index...")
        self.styles = {}
        for style in self.kml.features[0].styles:
            self.styles[style.id] = style
        print(f"loaded {len(self.styles)} styles")

    def convert_color(self, color: str):
        r = color[6:8]
        g = color[4:6]
        b = color[2:4]
        a = color[:2]

        return r + g + b + a

    def getPoints(self):
        points = []
        for placemark in self.placemarks:
            point = placemark.geometry
            if isinstance(point, Point):
                points.append((point.coords[0][1], point.coords[0][0], placemark.name, placemark.description))
        return points

    def getPolygons(self, progress_callback = None, point_length = None):
        polygons = []
        for i, placemark in enumerate(self.placemarks):
            # if i > 200:
            #     break
            polygon = placemark.geometry
            styleurl = placemark.style_url
            if not isinstance(polygon, MultiPolygon) and not isinstance(polygon, Polygon):
                continue
            styles = self.styles[styleurl.url[1:]]
            if isinstance(styles, StyleMap):
                styles = self.styles[styles.pairs[0].style.url[1:]]
            # stylemap = self.kml.features[0].get_style_by_url(styleurl.url)
            # normal_style_url = stylemap.pairs[0].style
            # normal_styles = self.kml.features[0].get_style_by_url(normal_style_url.url).styles
            for style in styles.styles:
                if isinstance(style, LineStyle):
                    linestyle = style
                if isinstance(style, PolyStyle):
                    polystyle = style

            if isinstance(polygon, MultiPolygon):
                for poly in polygon.geoms:
                    points = []
                    for point in poly.exterior.coords:
                        points.append((point[1], point[0]))
                    polygons.append((points, placemark.name, placemark.description, (self.convert_color(linestyle.color), linestyle.width), self.convert_color(polystyle.color)))
            if isinstance(polygon, Polygon):
                points = []
                for point in polygon.exterior.coords:
                    points.append((point[1], point[0]))
                polygons.append((points, placemark.name, placemark.description, (self.convert_color(linestyle.color), linestyle.width), self.convert_color(polystyle.color)))
            if i % 200 == 0:
                if progress_callback:
                    progress_callback.emit(50 + int(((i + 1) / len(self.placemarks) + point_length / len(self.placemarks)) * 25), "")
        return polygons

if __name__ == "__main__":
    kmlr = KMLReader(kml_path="C:\\Users\\David\\Documents\\DD Touren Test.kml")
    kmlr.loadKML()
    kmlr.getPolygons()