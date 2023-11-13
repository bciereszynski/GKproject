from PyQt5.QtCore import Qt

from BézierCurve.Curve import Curve
from Point import Point
from Primitives.DrawBox import DrawBox


class CurveDrawBox(DrawBox):
    def __init__(self):
        super().__init__()

        self.selectedObject = None
        self.__move = False
        self.__initial_pos = None

        self.completeSig = None
        self.stopEditSig = None

    def selectObject(self, obj, selected=True):
        if selected:
            self.selectedObject = obj
            obj.setSelected(True)
        else:
            self.selectedObject = None
            obj.setSelected(False)
            self.__move = False

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
                self.selectObject(p, True)
                self.__move = True
                self.__initial_pos = position
                self.editSig()
                return

        current = self.objectsList[-1]
        if type(current) == Curve and not current.isComplete():
            current.addPoint(Point(position.x(), position.y()))
            if current.isComplete():
                self.completeSig()

    def mouseMoveEvent(self, event):
        if self.__move:
            delta = event.pos() - self.__initial_pos
            self.selectedObject.move(delta)
            self.__initial_pos = event.pos()
            self.editSig()
            self.update()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.__move = False
