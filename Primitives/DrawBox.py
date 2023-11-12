
from PyQt5 import QtCore, QtGui, QtWidgets
import pickle


class DrawBox(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(DrawBox, self).__init__(parent)
        self.setBackgroundRole(QtGui.QPalette.Base)
        self.setAutoFillBackground(True)
        self.setMouseTracking(True)

        self.objectsList = []
        self.objectSelected = None

    def saveData(self, fileName="data.txt"):
        with open(fileName, "wb") as outfile:
            pickle.dump(self.objectsList, outfile)

    def loadData(self, fileName="data.txt"):
        with open(fileName, "rb") as infile:
            self.objectsList = pickle.load(infile)
        for sh in self.objectsList:
            sh.setSelected(False)
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtCore.Qt.darkCyan)
        for sh in self.objectsList:
            sh.render(painter)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if self.objectSelected is not None:
            self.objectSelected.setSelected(False)
            self.objectSelected = None
