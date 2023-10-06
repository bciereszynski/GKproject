from DataMenu import DataMenu
from DrawBox import DrawBox
from ShapesMenu import ShapesMenu
from PyQt5.QtWidgets import QLabel, QCheckBox
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt


class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setGeometry(QtCore.QRect(200, 100, 1200, 600))
        self.setWindowTitle("GK")

        self.paint = DrawBox()
        try:
            self.paint.loadData("data.txt")
        except:
            print("Error - file does not exists")

        self.menu = ShapesMenu(self.paint)
        self.dataMenu = DataMenu(self.paint)
        self.paint.readyToEditSignal = self.menu.editSlot
        self.sizeLabel = QLabel()
        self.sizeLabel.setFixedSize(150, 50)
        self.clickCreateCheck = QCheckBox("Click create")
        self.clickCreateCheck.stateChanged.connect(self.paint.setClickCreate)

        self.lay = QtWidgets.QHBoxLayout()
        self.lay.addWidget(self.paint, stretch=2)

        self.menuLay = QtWidgets.QVBoxLayout()
        self.menuLay.addWidget(self.menu, stretch=0)
        self.menuLay.addWidget(self.dataMenu, stretch=0)
        self.lay.addLayout(self.menuLay)

        self.sideLay = QtWidgets.QVBoxLayout()
        self.sideLay.addWidget(self.sizeLabel, stretch=0)
        self.sideLay.addWidget(self.clickCreateCheck, stretch=0)
        self.lay.addLayout(self.sideLay)

        self.lay.setAlignment(self.menuLay, Qt.AlignTop)
        self.lay.setAlignment(self.sideLay, Qt.AlignTop)
        self.setLayout(self.lay)

    def resizeEvent(self, a0):
        self.sizeLabel.setText(f"Field size: {self.paint.width()}, {self.paint.height()}")
