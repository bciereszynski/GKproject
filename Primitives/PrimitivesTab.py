from Primitives.DataMenu import DataMenu
from Primitives.PrimitivesDrawBox import PrimitivesDrawBox
from Primitives.ShapesMenu import ShapesMenu
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt


class PrimitivesTab(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(PrimitivesTab, self).__init__(parent)

        self.paint = PrimitivesDrawBox()
        self.menu = ShapesMenu(self.paint)
        self.dataMenu = DataMenu(self.paint)

        self.paint.readyToEditSignal = self.menu.EditState  # connect
        self.paint.stopEditSignal = self.menu.NotEditState  # connect

        self.lay = QtWidgets.QHBoxLayout()
        self.lay.addWidget(self.paint, stretch=2)

        self.menuLay = QtWidgets.QVBoxLayout()
        self.menuLay.addWidget(self.menu, stretch=0)
        self.menuLay.addWidget(self.dataMenu, stretch=0)
        self.lay.addLayout(self.menuLay)

        self.lay.setAlignment(self.menuLay, Qt.AlignTop)
        self.setLayout(self.lay)
