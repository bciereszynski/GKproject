from Primitives.DataMenu import DataMenu
from Primitives.DrawBox import DrawBox
from Primitives.ShapesMenu import ShapesMenu
from PyQt5.QtWidgets import QLabel
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt


class PrimitivesTab(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(PrimitivesTab, self).__init__(parent)

        self.paint = DrawBox()
        self.menu = ShapesMenu(self.paint)
        self.dataMenu = DataMenu(self.paint)

        self.paint.readyToEditSignal = self.menu.editSlot  # connect
        self.paint.stopEditSignal = self.menu.stopEditSlot  # connect

        self.sizeLabel = QLabel()
        self.sizeLabel.setFixedSize(150, 50)

        self.lay = QtWidgets.QHBoxLayout()
        self.lay.addWidget(self.paint, stretch=2)

        self.menuLay = QtWidgets.QVBoxLayout()
        self.menuLay.addWidget(self.menu, stretch=0)
        self.menuLay.addWidget(self.dataMenu, stretch=0)
        self.lay.addLayout(self.menuLay)

        self.sideLay = QtWidgets.QVBoxLayout()
        self.sideLay.addWidget(self.sizeLabel, stretch=0)
        self.lay.addLayout(self.sideLay)

        self.lay.setAlignment(self.menuLay, Qt.AlignTop)
        self.lay.setAlignment(self.sideLay, Qt.AlignTop)
        self.setLayout(self.lay)

    def resizeEvent(self, a0):
        self.sizeLabel.setText(f"Field size: {self.paint.width()}, {self.paint.height()}")
