from PyQt5.QtCore import Qt

from BézierCurve.Curve import Curve
from Point import Point
from Primitives.DrawBox import DrawBox


class CurveDrawBox(DrawBox):
    def __init__(self):
        super().__init__()

        self.__objectToMove = None
        self.__selectedCurve = None
        self.__initial_pos = None

        c = Curve(2)
        c.addPoint(Point(5, 5))
        c.addPoint(Point(100,100))
        self.objectsList.append(c)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)

        if event.button() == Qt.LeftButton:
            self.__mouseLeftClickHandle(event.pos())

        self.update()

    def __mouseLeftClickHandle(self, position):
        for sh in reversed(self.objectsList):
            ok, p = sh.contains(position)
            if p is not None:
                self.__objectToMove = p
                self.__selectedCurve = sh
                self.__initial_pos = position
                sh.setSelected(True, p)
                break

    def mouseMoveEvent(self, event):
        if self.__objectToMove is not None:
            delta = event.pos() - self.__initial_pos
            self.__objectToMove.move(delta)
            self.__selectedCurve.curvePoints = None
            self.__initial_pos = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.__objectToMove = None
