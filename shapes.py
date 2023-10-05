from PyQt5 import QtCore


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def render(self, painter):
        rect = QtCore.QRect(QtCore.QPoint(self.x-2,self.y-2), QtCore.QSize(6,6))
        painter.drawRect(rect)
