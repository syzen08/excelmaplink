import logging

from src.excel.region import Region
from src.excel.util import region_from_map_name


class CurrentRegions:
    def __init__(self, regions: list[Region], length: int, main_window):
        self.regions = regions
        self.length = length
        self.main_window = main_window
        self.logger = logging.getLogger("eml.spreadsheet.cur_regions")
        
        self.ensure_length()
        self.sort()
    
    def ensure_length(self):
        if len(self.regions) < self.length:
            self.logger.debug(f"padding from {len(self.regions)} to {self.length} regions")
            self.regions.extend([None] * (self.length - len(self.regions)))
        elif len(self.regions) > self.length:
            self.logger.debug(f"trimming from {len(self.regions)} to {self.length} regions")
            self.regions = self.regions[:self.length]
            
    def sort(self):
        self.regions.sort(key=lambda x: x is None)
    
    def update_highligts(self):
        self.main_window.map.map_bridge.reset_highlight()
        for region in self.regions:
            if region is None:
                continue
            self.main_window.map.map_bridge.highlight_region(region.map_name)
            
    def toggle_region(self, region_map_name: str):
        region = next((r for r in self.regions if r is not None and r.map_name == region_map_name), None)
        if region is not None:
            self.regions[self.regions.index(region)] = None
            self.logger.debug(f"removed region {region_map_name}")
            self.update_highligts()
            return
        if region is None:
            self.logger.debug(f"adding region {region_map_name}")
            self.regions[self.regions.index(None)] = region_from_map_name(region_map_name, self.main_window.spreadsheet.config, self.main_window.spreadsheet.region_sheet)
            self.update_highligts()