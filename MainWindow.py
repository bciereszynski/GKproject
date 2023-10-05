from DataMenu import DataMenu
from DrawBox import DrawBox
from ShapesMenu import ShapesMenu
from PyQt5.QtWidgets import QLabel
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt


class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setGeometry(QtCore.QRect(200, 100, 1200, 600))
        self.setWindowTitle("GK")

        self.paint = DrawBox()
        self.menu = ShapesMenu(self.paint)
        self.sizeLabel = QLabel()
        self.sizeLabel.setFixedSize(150, 50)

        self.dataMenu = DataMenu(self.paint)

        self.lay = QtWidgets.QHBoxLayout()
        self.lay.addWidget(self.paint, stretch=2)
        self.menuLay = QtWidgets.QVBoxLayout()
        self.menuLay.addWidget(self.menu, stretch=0)
        self.menuLay.addWidget(self.dataMenu, stretch=0)
        self.lay.addLayout(self.menuLay)
        self.lay.addWidget(self.sizeLabel, stretch=0)
        self.lay.setAlignment(self.menuLay, Qt.AlignTop)
        self.lay.setAlignment(self.sizeLabel, Qt.AlignTop)
        self.setLayout(self.lay)

    def resizeEvent(self, a0):
        self.sizeLabel.setText(f"Field size: {self.paint.width()}, {self.paint.height()}")
