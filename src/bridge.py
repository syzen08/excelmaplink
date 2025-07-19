from bs4 import BeautifulSoup
from PySide6.QtCore import QObject, Signal, Slot


class MapBridge(QObject):
    highlight_region = Signal(str)
    region_clicked_signal = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
    
    @Slot(str)
    def region_clicked(self, region_name: str):
        region_name = BeautifulSoup(region_name, "html.parser").get_text(strip=True).strip()
        self.region_clicked_signal.emit(region_name)
        
    @Slot(str)
    def _emit_highlight_region(self, region_name: str):
        print(f"highlighting region: {region_name}")
        self.highlight_region.emit(region_name)