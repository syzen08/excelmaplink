from PySide6.QtCore import QAbstractListModel

class MapRegionModel(QAbstractListModel):
    def __init__(self, regions: dict):
        QAbstractListModel.__init__(self)

        self.__regions = regions
        
