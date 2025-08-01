import warnings

# hide pretty print warning, as installing lxml breaks everything
with warnings.catch_warnings(action="ignore"):
    from fastkml import Placemark, kml
    from fastkml.styles import LineStyle, PolyStyle, StyleMap
    from fastkml.utils import find_all

from pygeoif.geometry import MultiPolygon, Point, Polygon
from PySide6.QtCore import QCoreApplication, QLoggingCategory, qCInfo


class KMLReader:
    def __init__(self, kml_path=None):
        self.kml_path = kml_path
        self.kml = None

    def loadKML(self, kml_path, progress_callback):
        if kml_path is not None:
            self.kml_path = kml_path
        
        if self.kml_path is None:
            raise Exception("No KML file specified")
        
        qCInfo(QLoggingCategory("kml"), f"parsing {self.kml_path}...")
        progress_callback.emit(QCoreApplication.translate("KMLReader", "parsing {}...").format(self.kml_path))
        self.kml = kml.KML.parse(self.kml_path)
        qCInfo(QLoggingCategory("kml"), "loading placemarks...")
        progress_callback.emit(QCoreApplication.translate("KMLReader", "loading placemarks..."))
        self.placemarks = list(find_all(self.kml, of_type=Placemark)) # TODO: reimplement using dictionary for faster loading
        qCInfo(QLoggingCategory("kml"), f"loaded {len(self.placemarks)} placemarks")
        progress_callback.emit(QCoreApplication.translate("KMLReader", "loading styles..."))
        qCInfo(QLoggingCategory("kml"), "creating style index...")
        self.styles = {}
        for style in self.kml.features[0].styles:
            self.styles[style.id] = style
        qCInfo(QLoggingCategory("kml"), f"loaded {len(self.styles)} styles")

    def convert_color(self, color: str) -> str:
        """Converts the colors from the format `#AABBGGRR` used in kml to the more standard `#RRGGBBAA`"""

        r = color[6:8]
        g = color[4:6]
        b = color[2:4]
        a = color[:2]

        return r + g + b + a

    def getPoints(self, points):
        # TODO: add style support
        # iterate through all placemarks
        qCInfo(QLoggingCategory("kml"), 'point process started')
        for i, placemark in enumerate(self.placemarks):
            point = placemark.geometry
            if isinstance(point, Point):
                points.append((point.coords[0][1], point.coords[0][0], placemark.name, placemark.description))
        qCInfo(QLoggingCategory("kml"), str(len(points)))


    def getPolygons(self, polygons):
        qCInfo(QLoggingCategory("kml"), 'polygon process started')
        for i, placemark in enumerate(self.placemarks):
            # if placemark is invisible, skip
            if placemark.visibility is False:
                continue
            polygon = placemark.geometry
            styleurl = placemark.style_url
            # if placemark is not a polygon, skip
            if not isinstance(polygon, MultiPolygon) and not isinstance(polygon, Polygon):
                continue

            # get style from style dict
            styles = self.styles[styleurl.url[1:]]
            # if style is a StyleMap, get the first style (usually the normal style) instead
            if isinstance(styles, StyleMap):
                styles = self.styles[styles.pairs[0].style.url[1:]]
            # seperate style types
            for style in styles.styles:
                if isinstance(style, LineStyle):
                    linestyle = style
                elif isinstance(style, PolyStyle):
                    polystyle = style
                else:
                    linestyle = None
                    polystyle = None

            # if linestyle or polystyle is not set, use default values
            if linestyle is None:
                linestyle = LineStyle(color="40000000", width=3.0)
            if polystyle is None:
                polystyle = PolyStyle(color="FFFF00FF")

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

        qCInfo(QLoggingCategory("kml"), str(len(polygons)))

if __name__ == "__main__":
    kmlr = KMLReader(kml_path="C:\\Users\\David\\Documents\\DD Touren Test.kml")
    kmlr.loadKML()
    kmlr.getPolygons()