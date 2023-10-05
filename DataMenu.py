from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QPushButton, QFileDialog


class DataMenu(QtWidgets.QWidget):

    def __init__(self, paint, parent=None):
        super(DataMenu, self).__init__(parent)
        self.setBackgroundRole(QtGui.QPalette.Window)
        self.setAutoFillBackground(True)
        self.resize = False
        self.setFixedWidth(300)
        self.setFixedHeight(100)

        self.paint = paint

        self.saveButton = QPushButton("Save")
        self.saveButton.clicked.connect(self.save)
        self.loadButton = QPushButton("Load")
        self.loadButton.clicked.connect(self.load)

        self.lay = QtWidgets.QVBoxLayout()
        self.lay.addWidget(self.saveButton)
        self.lay.addWidget(self.loadButton)
        self.setLayout(self.lay)

    def save(self):
        fileName = QFileDialog.getSaveFileName(self)
        self.paint.saveData(fileName[0])

    def load(self):
        fileName = QFileDialog.getOpenFileName(self)
        self.paint.loadData(fileName[0])
