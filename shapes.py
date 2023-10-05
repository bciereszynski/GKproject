from PyQt5 import QtCore
from PyQt5.QtCore import QPoint


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def render(self, painter):
        rect = QtCore.QRect(QtCore.QPoint(self.x-3,self.y-3), QtCore.QSize(6,6))
        painter.drawRect(rect)

    def resize(self, delta):
        self.x += delta.x()
        self.y += delta.y()

    def contains(self, point):
        max_x = self.x+3
        min_x = self.x-3
        max_y = self.y+3
        min_y = self.y-3
        if min_x < point.x() < max_x and min_y < point.y() < max_y:
            return True
        return False

class Rectangle:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def render(self, painter):
        rect = QtCore.QRect(QPoint(self.point1.x, self.point1.y), QPoint(self.point2.x, self.point2.y))
        self.point1.render(painter)
        self.point2.render(painter)
        painter.drawRect(rect)

    def resize(self, delta):
        self.point2.resize(delta)

    def contains(self, position):
        max_x = max(self.point1.x, self.point2.x)
        min_x = min(self.point1.x, self.point2.x)
        max_y = max(self.point1.y, self.point2.y)
        min_y = min(self.point1.y, self.point2.y)
        if min_x < position.x() < max_x and min_y < position.y() < max_y:
            return True
        return False

    def checkResize(self, position):
        if not self.contains(position) and self.point2.contains(position):
            return True
        return False

    def checkMove(self, position):
        if self.contains(position):
            return True
        return False
