from PyQt5.QtWidgets import QWidget, QHBoxLayout

from Transformations2D.PolygonDrawBox import PolygonDrawBox
from Transformations2D.PolygonMenu import PolygonMenu


class PolygonTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lay = QHBoxLayout()
        self.setLayout(self.lay)

        self.paintBox = PolygonDrawBox()
        self.lay.addWidget(self.paintBox)

        self.menu = PolygonMenu(self.paintBox)
        self.lay.addWidget(self.menu)
