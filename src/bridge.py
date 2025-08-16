import logging

from bs4 import BeautifulSoup
from PySide6.QtCore import QObject, Signal, Slot


class MapBridge(QObject):
    """allows communication between the leaflet map and this python code.
    to use, publish an instance of this over the qwebchannel"""
    highlight_region_signal = Signal(str)
    region_clicked_signal = Signal(str)
    reset_highlight_signal = Signal()
    finished_loading_signal = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = logging.getLogger("eml.map.bridge")
    
    @Slot(str)
    def region_clicked(self, region_name: str):
        region_name = BeautifulSoup(region_name, "html.parser").get_text(strip=True).strip()
        self.region_clicked_signal.emit(region_name)
        
    @Slot(str)
    def highlight_region(self, region_name: str):
        self.logger.info(f"highlighting region: {region_name}")
        self.highlight_region_signal.emit(region_name)
    
    @Slot()
    def finished_loading(self):
        self.logger.info("finished loading")
        self.finished_loading_signal.emit()
        
    def reset_highlight(self):
        self.logger.info("resetting highlight")
        self.reset_highlight_signal.emit()
    