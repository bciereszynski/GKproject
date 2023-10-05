from DrawBox import DrawBox
from Menu import Menu
from PyQt5.QtWidgets import QLabel
from PyQt5 import QtCore, QtWidgets

class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setGeometry(QtCore.QRect(200, 100, 1200, 600))
        self.sizeLabel = QLabel()
        self.sizeLabel.setFixedSize(150,50)
        self.paint = DrawBox()
        self.menu = Menu(self.paint)
        self.sizeHint()
        self.lay = QtWidgets.QHBoxLayout()
        self.lay.addWidget(self.paint, stretch=2)
        self.lay.addWidget(self.menu, stretch=0)
        self.lay.addWidget(self.sizeLabel, stretch=0)
        self.setLayout(self.lay)

    def resizeEvent(self, a0):
        self.sizeLabel.setText(f"Field size: {self.paint.width()}, {self.paint.height()}")