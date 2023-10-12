from PyQt5 import QtCore, QtGui, QtWidgets
import pickle

from PyQt5.QtCore import Qt

from Primitives.shapes import Line, Rectangle, Circle, Point


class DrawBox(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(DrawBox, self).__init__(parent)
        self.setBackgroundRole(QtGui.QPalette.Base)
        self.setAutoFillBackground(True)
        self.setMouseTracking(True)

        self.shapeType = "Line"

        self.shapesList = []

        self._objectToMove = None
        self._objectToResize = None
        self.shapeSelected = None
        self._initial_pos = None

        self.readyToEditSignal = None
        self.stopEditSignal = None

    def saveData(self, fileName="data.txt"):
        with open(fileName, "wb") as outfile:
            # "wb" argument opens the file in binary mode
            pickle.dump(self.shapesList, outfile)

    def loadData(self, fileName="data.txt"):
        with open(fileName, "rb") as infile:
            # "wb" argument opens the file in binary mode
            self.shapesList = pickle.load(infile)
            for sh in self.shapesList:
                sh.setSelected(False)
        self.update()

    def setShapeType(self, name):
        self.shapeType = name

    def showEvent(self, event):
        super(DrawBox, self).showEvent(event)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtCore.Qt.darkCyan)
        for sh in self.shapesList:
            sh.render(painter)

    def mousePressEvent(self, event):
        if self.shapeSelected is not None:
            self.shapeSelected.setSelected(False)
            self.shapeSelected = None

        if event.button() == Qt.LeftButton:
            self.mouseLeftClickHandle(event.pos())

        if event.button() == Qt.RightButton:
            self.mouseRightClickHandle(event.pos())

        if self.shapeSelected is None:
            self.emitStopEdit()
        else:
            self.shapeSelected.setSelected(True)
        self.update()

        super(DrawBox, self).mousePressEvent(event)

    def mouseLeftClickHandle(self, position):
        for sh in reversed(self.shapesList):
            if sh.checkResize(position):
                self._objectToResize = sh
                self.shapeSelected = sh
                self.emitReadyToEdit()
                self._initial_pos = position
                break
            if sh.checkMove(position):
                self._objectToMove = sh
                self.shapeSelected = sh
                self.emitReadyToEdit()
                self._initial_pos = position
                break

    def mouseRightClickHandle(self, position):
        self.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        point1 = Point(position.x(), position.y())
        point2 = Point(position.x(), position.y())
        self.createShape(point1, point2)
        self._initial_pos = position
        self._objectToResize = self.shapesList[-1]
        self.shapeSelected = self.shapesList[-1]
        self.emitReadyToEdit()

    def mouseMoveEvent(self, event):
        if self._objectToResize is not None:
            delta = event.pos() - self._initial_pos
            self._objectToResize.resize(delta)
            self._initial_pos = event.pos()
            self.emitReadyToEdit()
            self.update()
        elif self._objectToMove is not None:
            delta = event.pos() - self._initial_pos
            self._objectToMove.move(delta)
            self.emitReadyToEdit()
            self.update()
            self._initial_pos = event.pos()
        else:
            self.determineCursor(event.pos())

        super(DrawBox, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self._objectToResize = None
        self._objectToMove = None
        self.determineCursor(event.pos())
        super(DrawBox, self).mouseReleaseEvent(event)

    def createShape(self, point1, point2):
        if self.shapeType == "Line":
            self.shapesList.append(Line(point1, point2))
        elif self.shapeType == "Rectangle":
            self.shapesList.append(Rectangle(point1, point2))
        elif self.shapeType == "Circle":
            self.shapesList.append(Circle(point1, point2))
        self.update()

    def editShape(self, point1, point2):
        self.shapeSelected.point1 = point1
        self.shapeSelected.point2 = point2
        self.update()

    def deleteShape(self):
        self.shapesList.remove(self.shapeSelected)
        self.update()

    def determineCursor(self, position):
        cursor = QtGui.QCursor(QtCore.Qt.ArrowCursor)
        for sh in reversed(self.shapesList):
            if sh.checkResize(position):
                cursor = QtGui.QCursor(QtCore.Qt.SizeAllCursor)
                break
            if sh.checkMove(position):
                cursor = QtGui.QCursor(QtCore.Qt.OpenHandCursor)
                break

        self.setCursor(cursor)

    def emitReadyToEdit(self):
        try:
            QtCore.QTimer.singleShot(0, self.readyToEditSignal)
        except:
            print("slot is not connected")

    def emitStopEdit(self):
        try:
            QtCore.QTimer.singleShot(0, self.stopEditSignal)
        except:
            print("slot is not connected")