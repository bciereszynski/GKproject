import numpy as np
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt

from Primitives.DrawBox import DrawBox
from Transformations2D.Vertex import Vertex


class PolygonDrawBox(DrawBox):
    def __init__(self):
        super().__init__()

        self.mode = None

        self.selectedObject = None
        self.__initial_pos = None
        self.calcPoint = Vertex(100, 100)
        self.objectsList.append(self.calcPoint)

        self.tempLine = None

        self.completeSig = None
        self.stopEditSig = None

    def drawLine(self, x1, y1, x2, y2):
        self.tempLine = (x1, y1, x2, y2)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtCore.Qt.darkCyan)
        if self.tempLine != None:
            painter.drawLine(*self.tempLine)
        self.tempLine = None


    def selectObject(self, obj, selected=True):
        if selected:
            self.selectedObject = obj
            obj.setSelected(True)
        else:
            self.selectedObject = None
            obj.setSelected(False)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)

        if event.button() == Qt.LeftButton:
            self.__mouseLeftClickHandle(event.pos())

        self.update()

    def __mouseLeftClickHandle(self, position):
        if self.selectedObject is not None:
            self.selectObject(self.selectedObject, False)
            self.stopEditSig()
        for sh in reversed(self.objectsList):
            p = sh.detectPoint(position)
            if p is not None:
                self.selectObject(sh, True)
                self.__initial_pos = position
                return

        current = self.objectsList[-1]
        if not current.isComplete():
            current.addPoint(Vertex(position.x(), position.y()))
            if current.isComplete():
                self.completeSig()

    def mouseMoveEvent(self, event):
        if self.__initial_pos is None:
            return
        self.update()
        self.drawLine(self.__initial_pos.x(), self.__initial_pos.y(), event.pos().x(), event.pos().y())

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if self.__initial_pos is None:
            return
        if self.mode == "trans":
            delta = event.pos() - self.__initial_pos
            self.selectedObject.move(delta)

        if self.mode == "rotate":
            angle = self.__calculateAngle(self.__initial_pos, self.calcPoint, event.pos())
            self.selectedObject.rotate(self.calcPoint.x, self.calcPoint.y, angle)

        if self.mode == "scale":
            factorX, factorY = self.__calculateFactors(self.__initial_pos, event.pos(), self.calcPoint)
            self.selectedObject.scale(self.calcPoint.x, self.calcPoint.y, factorX, factorY)

        self.selectObject(self.selectedObject, False)
        self.__initial_pos = None
        self.update()

    @staticmethod
    def __calculateFactors(startPoint, destPoint, calcPoint):
        factorX = abs(destPoint.x() - calcPoint.x) / abs(startPoint.x() - calcPoint.x)
        factorY = abs(destPoint.y() - calcPoint.y) / abs(startPoint.y() - calcPoint.y)
        return factorX, factorY

    @staticmethod
    def __calculateAngle(pointA, pointB, pointC):
        a = np.array([pointA.x(), pointA.y()])
        b = np.array([pointB.x, pointB.y])
        c = np.array([pointC.x(), pointC.y()])

        ba = a - b
        bc = c - b

        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        angle = np.arccos(cosine_angle)

        return np.degrees(angle)
