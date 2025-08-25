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
        # validate path
        self.kml_path = kml_path
        if self.kml_path is None:
            raise FileNotFoundError("no kml file specified")
        if self.kml_path.suffix.lower() not in [".kml", ".kmz"]:
            raise ValueError(f"invalid extension: {self.kml_path.suffix}. must be .kml or .kmz")
        
        if self.kml_path.suffix == ".kmz":
            self.logger.debug("kmz, opening zip and reading in doc...")
            with ZipFile(str(self.kml_path)) as zip_file, zip_file.open("doc.kml") as kml_doc:
                doc = kml_doc.read()
        else:
            self.logger.debug("kml, reading in doc...")
            with self.kml_path.open("r", encoding="utf-8") as f:
                doc = f.read()
        
        self.logger.info(f"parsing {self.kml_path}...")
        progress_callback.emit(QCoreApplication.translate("KMLReader", "parsing {}...").format(self.kml_path))
        self.kml = kml.KML.from_string(doc)
        
        self.logger.info("loading placemarks...")
        progress_callback.emit(QCoreApplication.translate("KMLReader", "loading placemarks..."))
        self.placemarks = list(find_all(self.kml, of_type=Placemark))
        self.logger.info(f"loaded {len(self.placemarks)} placemarks")
        
        # copy all styles into a dict, this is faster than fastkml's get_style_by_url().
        progress_callback.emit(QCoreApplication.translate("KMLReader", "loading styles..."))
        self.logger.info("creating style index...")
        self.styles = {}
        for style in self.kml.features[0].styles:
            self.styles[style.id] = style
        self.logger.info(f"loaded {len(self.styles)} styles")

    def convert_color(self, color: str) -> str:
        """Converts the colors from the format `#AABBGGRR` used in kml to the more standard `#RRGGBBAA`"""
        if color is None:
            return None
        
        r = color[6:8]
        g = color[4:6]
        b = color[2:4]
        a = color[:2]

        return r + g + b + a

    def getPoints(self, points: list, ret: bool = False) -> None | list[tuple]:
        """get all points from the kml and saves them into the provided list. if ret is True, return the list as well.
        every point is a tuple of the following format:
        ( 0: lat, 1: long, 2: name, 3: description, 4: icon, 5: icon color )"""
        # iterate through all placemarks
        self.logger.debug("getting points...")
        for placemark in self.placemarks:
            # skip anything that isn't a point
            if not isinstance(placemark, Point):
                continue
            
            # if not visible, skip
            if placemark.visibility is False:
                continue
            
            point = placemark.geometry
            styleurl = placemark.style_url
            # get style from the index
            styles = self.styles[styleurl.url[1:]]
            # if its a StyleMap, get the first style from there, usually the "normal" one
            if isinstance(styles, StyleMap):
                styles = self.styles[styles.pairs[0].style.url[1:]]
            
            for style in styles.styles:
                if isinstance(style, IconStyle):
                    iconstyle: IconStyle = style
                    icon = self.match_icon(iconstyle.icon_href)
                    self.logger.debug(f"href: {iconstyle.icon_href}, icon_match: {icon}")
                    break
                iconstyle = IconStyle()
                icon = None
                    
            points.append((point.coords[0][1], point.coords[0][0], placemark.name, placemark.description, icon, self.convert_color(iconstyle.color)))
        self.logger.info(str(len(points)))
        if ret:
            return points
        return None


    def getPolygons(self, polygons: list, ret: bool = False) -> None | list[tuple]:
        """gets all points from the kml and saves them into the provided list. if ret is True, return the list as well.
        every polygon is a tuple of the following format:
        ( 0: [ ( lat, long ), ( lat, long ), ... ], 1: name, 2: description, 3: outline color, 4: outline width, 5: fill color )"""
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
            
            points = []
            if isinstance(polygon, MultiPolygon):
                for poly in polygon.geoms:
                    for point in poly.exterior.coords:
                        points.append((point[1], point[0]))
            if isinstance(polygon, Polygon):
                for point in polygon.exterior.coords:
                    points.append((point[1], point[0]))

            polygons.append((points, placemark.name, placemark.description, (self.convert_color(linestyle.color), linestyle.width), self.convert_color(polystyle.color)))

        self.logger.info(str(len(polygons)))
        if ret:
            return polygons
        return None
        
    def match_icon(self, icon_href) -> str:
        """matches some google earth icons with the corresponding font awesome icons"""
        icon_map = {
            "http://maps.google.com/mapfiles/kml/shapes/truck.png": "truck",
            "http://maps.google.com/mapfiles/kml/shapes/ranger_station.png": "house", 
            "http://maps.google.com/mapfiles/kml/shapes/info.png": "info", 
            "http://maps.google.com/mapfiles/kml/shapes/flag.png": "flag", 
            "http://maps.google.com/mapfiles/kml/shapes/cabs.png": "taxi", 
            "http://maps.google.com/mapfiles/kml/shapes/caution.png": "triangle-exclamation", 
            "http://maps.google.com/mapfiles/kml/shapes/parking_lot.png": "square-parking", 
            "http://maps.google.com/mapfiles/kml/shapes/phone.png": "phone", 
            "http://maps.google.com/mapfiles/kml/shapes/euro.png": "euro-sign", 
            "http://maps.google.com/mapfiles/kml/shapes/post_office.png": "envelope", 
            "http://maps.google.com/mapfiles/kml/shapes/forbidden.png": "ban", 
            "http://maps.google.com/mapfiles/kml/shapes/info_circle.png": "circle-question", 
            "http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png": "default", 
        }
        return icon_map.get(icon_href, f"custom {icon_href}")
