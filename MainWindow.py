from DrawBox import DrawBox
from Menu import ShapesMenu
from PyQt5.QtWidgets import QLabel
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt


class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setGeometry(QtCore.QRect(200, 100, 1200, 600))
        self.setWindowTitle("GK")
        self.sizeLabel = QLabel()
        self.sizeLabel.setFixedSize(150, 50)

        self.paint = DrawBox()
        self.menu = ShapesMenu(self.paint)

        self.lay = QtWidgets.QHBoxLayout()
        self.lay.addWidget(self.paint, stretch=2)
        self.lay.addWidget(self.menu, stretch=0)
        self.lay.addWidget(self.sizeLabel, stretch=0)
        self.lay.setAlignment(self.menu, Qt.AlignTop)
        self.lay.setAlignment(self.sizeLabel, Qt.AlignTop)
        self.setLayout(self.lay)

    def resizeEvent(self, a0):
        self.sizeLabel.setText(f"Field size: {self.paint.width()}, {self.paint.height()}")
