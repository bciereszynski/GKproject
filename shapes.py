from PyQt5 import QtCore


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def render(self, painter):
        rect = QtCore.QRect(QtCore.QPoint(self.x,self.y), QtCore.QSize(5,5))
        painter.drawRect(rect)
