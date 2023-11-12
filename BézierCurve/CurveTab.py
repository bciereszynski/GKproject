from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

from BézierCurve.CurveDrawBox import CurveDrawBox
from BézierCurve.CurveMenu import CurveMenu


class CurveTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lay = QHBoxLayout()
        self.setLayout(self.lay)

        self.paintBox = CurveDrawBox()
        self.lay.addWidget(self.paintBox)

        self.menu = CurveMenu(self.paintBox)
        self.lay.addWidget(self.menu)
