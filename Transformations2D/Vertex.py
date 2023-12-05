import numpy as np
from PyQt5 import QtGui, QtCore


class Vertex:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.isSelected = False
        self.parent = None

    def render(self, painter, selected=None):
        if selected is None:
            selected = self.isSelected
        tempBrush = painter.brush()
        tempPen = painter.pen()
        if selected:
            painter.setBrush(QtGui.QBrush(QtCore.Qt.red))
            painter.setPen(QtCore.Qt.darkRed)
        else:
            painter.setBrush(QtGui.QBrush(QtCore.Qt.green))
            painter.setPen(QtCore.Qt.darkGreen)
        rect = QtCore.QRect(QtCore.QPoint(self.x-3, self.y-3), QtCore.QSize(6, 6))
        painter.drawRect(rect)
        painter.setBrush(tempBrush)
        painter.setPen(tempPen)

    def setX(self, value):
        self.x = value
        if self.parent is not None:
            self.parent.update()

    def setY(self, value):
        self.y = value
        if self.parent is not None:
            self.parent.update()

    def setSelected(self, isSelected):
        self.isSelected = isSelected

    def move(self, delta):
        pointMatrix = np.array([self.x, self.y, 1]).reshape(3, 1)
        translationMatrix = np.array([1, 0, delta.x(), 0, 1, delta.y(), 0, 0, 1]).reshape(3, 3)

        result = np.matmul(translationMatrix, pointMatrix)

        self.x = result[0, 0]
        self.y = result[1, 0]

    def rotate(self, x, y, angle):
        angle = np.pi/180 * angle
        pointMatrix = np.array([self.x - x, self.y - y, 1]).reshape(3, 1)
        translationMatrix = np.array([np.cos(angle), -np.sin(angle), 0, np.sin(angle), np.cos(angle),
                                      0, 0, 0, 1]).reshape(3, 3)

        result = np.matmul(translationMatrix, pointMatrix)
        try:
            self.x = x + int(result[0, 0])
        except:
            pass
        try:
            self.y = y + int(result[1, 0])
        except:
            pass

    def scale(self, x, y, factorX, factorY):
        pointMatrix = np.array([self.x - x, self.y - y, 1]).reshape(3, 1)
        translationMatrix = np.array([factorX, 0, 0, 0, factorY, 0, 0, 0, 1]).reshape(3, 3)

        result = np.matmul(translationMatrix, pointMatrix)
        try:
            self.x = x + int(result[0, 0])
        except:
            pass
        try:
            self.y = y + int(result[1, 0])
        except:
            pass

    def resize(self, delta):
        self.move(delta)

    def contains(self, point):
        max_x = self.x+3
        min_x = self.x-3
        max_y = self.y+3
        min_y = self.y-3
        if min_x < point.x() < max_x and min_y < point.y() < max_y:
            return True
        return

    def detectPoint(self, position):
        if self.contains(position):
            return self
        else:
            return None

    def isComplete(self):
        return True

    @staticmethod
    def __multiplyMatrix(A, B):
        return [[sum(a*b for a, b in zip(A_row, B_col)) for B_col in zip(*B)] for A_row in A]
