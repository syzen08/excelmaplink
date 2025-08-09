import logging
import warnings
from pathlib import Path
from zipfile import ZipFile

# hide pretty print warning, as installing lxml breaks everything
with warnings.catch_warnings(action="ignore"):
    from fastkml import Placemark, kml
    from fastkml.styles import IconStyle, LineStyle, PolyStyle, StyleMap
    from fastkml.utils import find_all

from pygeoif.geometry import MultiPolygon, Point, Polygon
from PySide6.QtCore import QCoreApplication


class KMLReader:
    def __init__(self, kml_path=None):
        self.kml_path = kml_path
        self.kml = None
        self.logger = logging.getLogger("eml.kml")

    def loadKML(self, kml_path: Path, progress_callback):
        if kml_path is not None:
            self.kml_path = kml_path
        
        if self.kml_path is None:
            raise FileNotFoundError("no kml file specified")
        
        if self.kml_path.suffix.lower() not in [".kml", ".kmz"]:
            raise ValueError(f"invalid extension: {self.kml_path.suffix}. must be .kml or .kmz")
        
        if self.kml_path.suffix == ".kmz":
            self.logger.debug("kmz, opening zip and reading in doc...")
            with ZipFile(str(self.kml_path)) as zip:
                with zip.open("doc.kml") as kml_doc:
                    doc = kml_doc.read()
        else:
            self.logger.debug("kml, reading in doc...")
            with open(str(self.kml_path)) as f:
                doc = f.read()
        
        self.logger.info(f"parsing {self.kml_path}...")
        progress_callback.emit(QCoreApplication.translate("KMLReader", "parsing {}...").format(self.kml_path))
        self.kml = kml.KML.from_string(doc)
        self.logger.info("loading placemarks...")
        progress_callback.emit(QCoreApplication.translate("KMLReader", "loading placemarks..."))
        self.placemarks = list(find_all(self.kml, of_type=Placemark)) # TODO: reimplement using dictionary for faster loading
        self.logger.info(f"loaded {len(self.placemarks)} placemarks")
        progress_callback.emit(QCoreApplication.translate("KMLReader", "loading styles..."))
        self.logger.info("creating style index...")
        self.styles = {}
        for style in self.kml.features[0].styles:
            self.styles[style.id] = style
        self.logger.info(f"loaded {len(self.styles)} styles")

    def convert_color(self, color: str) -> str:
        """Converts the colors from the format `#AABBGGRR` used in kml to the more standard `#RRGGBBAA`"""
        if color is None:
            return
        
        r = color[6:8]
        g = color[4:6]
        b = color[2:4]
        a = color[:2]

        return r + g + b + a

    def getPoints(self, points: list, ret: bool = False):
        # TODO: add style support
        # iterate through all placemarks
        self.logger.debug('getting points...')
        for i, placemark in enumerate(self.placemarks):
            point = placemark.geometry
            styleurl = placemark.style_url
            
            styles = self.styles[styleurl.url[1:]]
            if isinstance(styles, StyleMap):
                styles = self.styles[styles.pairs[0].style.url[1:]]
            
            for style in styles.styles:
                if isinstance(style, IconStyle):
                    iconstyle: IconStyle = style
                    icon = self.match_icon(iconstyle.icon_href)
                    self.logger.debug(f"href: {iconstyle.icon_href}, icon_match: {icon}")
                    break
                else:
                    iconstyle = IconStyle()
                    icon = None
                    
            if isinstance(point, Point):
                points.append((point.coords[0][1], point.coords[0][0], placemark.name, placemark.description, icon, self.convert_color(iconstyle.color)))
        self.logger.info(str(len(points)))
        if ret:
            return points


    def getPolygons(self, polygons: list, ret: bool = False):
        self.logger.debug('getting polygons...')
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

        self.logger.info(str(len(polygons)))
        if ret:
            return polygons
        
    def match_icon(self, icon_href) -> str:
        """matches some google earth icons with the corresponding font awesome icons"""
        match icon_href:
            case "http://maps.google.com/mapfiles/kml/shapes/truck.png":
                return "truck"
            case "http://maps.google.com/mapfiles/kml/shapes/ranger_station.png":
                return "house"
            case "http://maps.google.com/mapfiles/kml/shapes/info.png":
                return "info"
            case "http://maps.google.com/mapfiles/kml/shapes/flag.png":
                return "flag"
            case "http://maps.google.com/mapfiles/kml/shapes/cabs.png":
                return "taxi"
            case "http://maps.google.com/mapfiles/kml/shapes/caution.png":
                return "triangle-exclamation"
            case "http://maps.google.com/mapfiles/kml/shapes/parking_lot.png":
                return "square-parking"
            case "http://maps.google.com/mapfiles/kml/shapes/phone.png":
                return "phone"
            case "http://maps.google.com/mapfiles/kml/shapes/euro.png":
                return "euro-sign"
            case "http://maps.google.com/mapfiles/kml/shapes/post_office.png":
                return "envelope"
            case "http://maps.google.com/mapfiles/kml/shapes/forbidden.png":
                return "ban"
            case "http://maps.google.com/mapfiles/kml/shapes/info_circle.png":
                return "circle-question"
            case "http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png":
                return "default"
            case _:
                return f"custom: {icon_href}"
                
            

if __name__ == "__main__":
    kmlr = KMLReader(kml_path="C:\\Users\\David\\Documents\\DD Touren Test.kml")
    kmlr.loadKML()
    kmlr.getPolygons()