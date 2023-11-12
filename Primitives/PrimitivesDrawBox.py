from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt

from Primitives.DrawBox import DrawBox
from Primitives.shapes import Line, Rectangle, Circle
from Point import Point


class PrimitivesDrawBox(DrawBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.shapeType = "Line"

        self._objectToMove = None
        self._objectToResize = None
        self._initial_pos = None

        self.readyToEditSignal = None
        self.stopEditSignal = None

    def setShapeType(self, name):
        self.shapeType = name

    def mousePressEvent(self, event):
        super().mousePressEvent(event)

        if event.button() == Qt.LeftButton:
            self.__mouseLeftClickHandle(event.pos())

        if event.button() == Qt.RightButton:
            self.__mouseRightClickHandle(event.pos())

        if self.objectSelected is None:
            self.emitStopEdit()
        else:
            self.objectSelected.setSelected(True)
        self.update()

    def __mouseLeftClickHandle(self, position):
        for sh in reversed(self.objectsList):
            if sh.checkResize(position):
                self._objectToResize = sh
                self.objectSelected = sh
                self.emitReadyToEdit()
                self._initial_pos = position
                break
            if sh.checkMove(position):
                self._objectToMove = sh
                self.objectSelected = sh
                self.emitReadyToEdit()
                self._initial_pos = position
                break

    def __mouseRightClickHandle(self, position):
        self.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        point1 = Point(position.x(), position.y())
        point2 = Point(position.x(), position.y())
        self.createShape(point1, point2)
        self._initial_pos = position
        self._objectToResize = self.objectsList[-1]
        self.objectSelected = self.objectsList[-1]
        self.emitReadyToEdit()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
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

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self._objectToResize = None
        self._objectToMove = None
        self.determineCursor(event.pos())

    def createShape(self, point1, point2):
        if self.shapeType == "Line":
            self.objectsList.append(Line(point1, point2))
        elif self.shapeType == "Rectangle":
            self.objectsList.append(Rectangle(point1, point2))
        elif self.shapeType == "Circle":
            self.objectsList.append(Circle(point1, point2))
        self.update()

    def editShape(self, point1, point2):
        self.objectSelected.point1 = point1
        self.objectSelected.point2 = point2
        self.update()

    def deleteShape(self):
        self.objectsList.remove(self.objectSelected)
        self.update()

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

    def determineCursor(self, position):
        cursor = QtGui.QCursor(QtCore.Qt.ArrowCursor)
        for sh in reversed(self.objectsList):
            if sh.checkResize(position):
                cursor = QtGui.QCursor(QtCore.Qt.SizeAllCursor)
                break
            if sh.checkMove(position):
                cursor = QtGui.QCursor(QtCore.Qt.OpenHandCursor)
                break
        self.setCursor(cursor)
