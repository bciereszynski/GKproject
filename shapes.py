from PyQt5 import QtCore
from PyQt5.QtCore import QPoint
import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def render(self, painter):
        rect = QtCore.QRect(QtCore.QPoint(self.x-3,self.y-3), QtCore.QSize(6,6))
        painter.drawRect(rect)

    def move(self, delta):
        self.x += delta.x()
        self.y += delta.y()

    def resize(self, delta):
        self.move(delta)

    def contains(self, point):
        max_x = self.x+3
        min_x = self.x-3
        max_y = self.y+3
        min_y = self.y-3
        if min_x < point.x() < max_x and min_y < point.y() < max_y:
            return True
        return False


class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
        self._resizePoint = None
        self._tolerance = 1

    def render(self, painter):
        self.point1.render(painter)
        self.point2.render(painter)
        painter.drawLine(self.point1.x, self.point1.y, self.point2.x, self.point2.y)

    def resize(self, delta):
        if self._resizePoint is not None:
            self._resizePoint.resize(delta)

    def move(self, delta):
        self.point1.move(delta)
        self.point2.move(delta)

    def contains(self, position):
        distP1P2 = math.sqrt(math.pow(self.point1.x-self.point2.x, 2) + math.pow(self.point1.y - self.point2.y, 2))
        distP1Poz = math.sqrt(math.pow(self.point1.x - position.x(), 2) + math.pow(self.point1.y - position.y(), 2))
        distP2Poz = math.sqrt(math.pow(self.point2.x - position.x(), 2) + math.pow(self.point2.y - position.y(), 2))

        if abs(distP1P2 - distP1Poz - distP2Poz) < self._tolerance:
            return True

        return False

    def checkResize(self, position):
        if self.point1.contains(position):
            self._resizePoint = self.point1
            return True
        if self.point2.contains(position):
            self._resizePoint = self.point2
            return True
        return False

    def checkMove(self, position):
        if self.contains(position) and not self.point2.contains(position):
            return True
        return False

class Rectangle:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
        self._resizePoint = None

    def render(self, painter):
        self.point1.render(painter)
        self.point2.render(painter)
        painter.drawRect(self.point1.x, self.point1.y, self.point2.x-self.point1.x, self.point2.y-self.point1.y)

    def resize(self, delta):
        if self._resizePoint != None:
            self._resizePoint.resize(delta)

    def move(self, delta):
        self.point1.move(delta)
        self.point2.move(delta)

    def contains(self, position):
        max_x = max(self.point1.x, self.point2.x)
        min_x = min(self.point1.x, self.point2.x)
        max_y = max(self.point1.y, self.point2.y)
        min_y = min(self.point1.y, self.point2.y)
        if min_x < position.x() < max_x and min_y < position.y() < max_y:
            return True
        return False

    def checkResize(self, position):
        if self.point1.contains(position):
            self._resizePoint = self.point1
            return True
        if self.point2.contains(position):
            self._resizePoint = self.point2
            return True
        return False

    def checkMove(self, position):
        if self.contains(position) and not self.point2.contains(position):
            return True
        return False
