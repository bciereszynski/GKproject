from PyQt5 import QtGui, QtCore


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def render(self, painter, selected=False):
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