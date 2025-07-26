from bs4 import BeautifulSoup
from PySide6.QtCore import QObject, Signal, Slot


class MapBridge(QObject):
    highlight_region_signal = Signal(str)
    region_clicked_signal = Signal(str)
    reset_highlight_signal = Signal()
    
    
    def __init__(self, parent=None):
        super().__init__(parent)
    
    @Slot(str)
    def region_clicked(self, region_name: str):
        region_name = BeautifulSoup(region_name, "html.parser").get_text(strip=True).strip()
        self.region_clicked_signal.emit(region_name)
        
    @Slot(str)
    def highlight_region(self, region_name: str):
        print(f"highlighting region: {region_name}")
        self.highlight_region_signal.emit(region_name)
        
    def reset_highlight(self):
        print("resetting highlight")
        self.reset_highlight_signal.emit()
    