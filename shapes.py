from PyQt5 import QtCore
from PyQt5.QtCore import QPoint


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def render(self, painter):
        rect = QtCore.QRect(QtCore.QPoint(self.x-2,self.y-2), QtCore.QSize(6,6))
        painter.drawRect(rect)

class Rectangle:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def render(self, painter):
        rect = QtCore.QRect(QPoint(self.point1.x, self.point1.y), QPoint(self.point2.x, self.point2.y))
        self.point1.render(painter)
        self.point2.render(painter)
        painter.drawRect(rect)