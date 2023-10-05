from PyQt5 import QtCore, QtGui, QtWidgets
import pickle

from shapes import Line, Rectangle, Circle, Point


class DrawBox(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(DrawBox, self).__init__(parent)
        self.setBackgroundRole(QtGui.QPalette.Base)
        self.setAutoFillBackground(True)
        self.setMouseTracking(True)

        self.shapeType = "Line"
        self.clickCreate = False

        self.shapes = []

        self._objectToMove = None
        self._objectToResize = None
        self._initial_pos = None

    def saveData(self, fileName="data.txt"):
        with open(fileName, "wb") as outfile:
            # "wb" argument opens the file in binary mode
            pickle.dump(self.shapes, outfile)

    def loadData(self, fileName="data.txt"):
        with open(fileName, "rb") as infile:
            # "wb" argument opens the file in binary mode
            self.shapes = pickle.load(infile)
        self.update()

    def setClickCreate(self, state):
        self.clickCreate = bool(state)

    def setShapeType(self, name):
        self.shapeType = name

    def showEvent(self, event):
        super(DrawBox, self).showEvent(event)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtCore.Qt.darkCyan)
        for sh in self.shapes:
            sh.render(painter)

    def mousePressEvent(self, event):
        if self.clickCreate:
            point1 = Point(event.pos().x(), event.pos().y())
            point2 = Point(event.pos().x(), event.pos().y())
            self._initial_pos = event.pos()
            self.createShape(point1, point2)
            self._objectToResize = self.shapes[-1]
            self.update()
        else:
            for sh in reversed(self.shapes):
                if sh.checkResize(event.pos()):
                    self._objectToResize = sh
                    self._initial_pos = event.pos()
                    break
                if sh.checkMove(event.pos()):
                    self._objectToMove = sh
                    self._initial_pos = event.pos()
                    break

        super(DrawBox, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._objectToResize is not None:
            delta = event.pos() - self._initial_pos
            self._objectToResize.resize(delta)
            self._initial_pos = event.pos()
            self.update()
        elif self._objectToMove is not None:
            delta = event.pos() - self._initial_pos
            self._objectToMove.move(delta)
            self.update()
            self._initial_pos = event.pos()
        elif self.clickCreate:
            self.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        else:
            for sh in reversed(self.shapes):
                if sh.checkMove(event.pos()):
                    self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
                    break
                if sh.checkResize(event.pos()):
                    self.setCursor(QtGui.QCursor(QtCore.Qt.SizeAllCursor))
                    break
                self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        super(DrawBox, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self._objectToResize = None
        self._objectToMove = None
        super(DrawBox, self).mouseReleaseEvent(event)

    def createShape(self, point1, point2):
        if self.shapeType == "Line":
            self.shapes.append(Line(point1, point2))
        elif self.shapeType == "Rectangle":
            self.shapes.append(Rectangle(point1, point2))
        elif self.shapeType == "Circle":
            self.shapes.append(Circle(point1, point2))
        self.update()
