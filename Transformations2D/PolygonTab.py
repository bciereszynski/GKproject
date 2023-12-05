from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout

from Primitives.DataMenu import DataMenu
from Transformations2D.PolygonDrawBox import PolygonDrawBox
from Transformations2D.PolygonMenu import PolygonMenu


class PolygonTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lay = QHBoxLayout()
        self.setLayout(self.lay)

        self.paintBox = PolygonDrawBox()
        self.lay.addWidget(self.paintBox)

        self.dataMenu = DataMenu(self.paintBox)
        self.menu = PolygonMenu(self.paintBox)

        menuLay = QVBoxLayout()
        menuLay.addWidget(self.menu)
        menuLay.addWidget(self.dataMenu)
        self.lay.addLayout(menuLay)
