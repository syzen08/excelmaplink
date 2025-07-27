from dataclasses import dataclass


@dataclass
class Region:
    excel_name: str
    map_name: str
    row: int
    
