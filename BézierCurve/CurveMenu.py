from PyQt5.QtWidgets import QVBoxLayout, QWidget, QInputDialog

from BézierCurve.Curve import Curve
from Point import Point
from Primitives.Menu import Menu


class CurveMenu(Menu):
    def __init__(self, drawBox):
        super().__init__()

        self.drawBox = drawBox

        self.createCurveBtn = self.createButton("Start making curve", self.createCurve)

        self.pointContainer = QWidget()
        pointLay = QVBoxLayout(self.pointContainer)
        self.pointXSpin, label = self.createSpinBox("Point x:", 2000, autoAdd=False)
        pointLay.addWidget(label)
        pointLay.addWidget(self.pointXSpin)
        self.pointYSpin, label = self.createSpinBox("Point y:", 1000, autoAdd=False)
        pointLay.addWidget(label)
        pointLay.addWidget(self.pointYSpin)
        self.addPointBtn = self.createButton("Add point", self.addPoint, autoAdd=False)
        pointLay.addWidget(self.addPointBtn)

        self.lay.addWidget(self.pointContainer)
        self.pointContainer.setEnabled(False)

        self.__currentCurve = None

    def createCurve(self):
        (value, ok) = QInputDialog().getInt(self, "Curve level", "Level:", 2, 2, 10)
        if not ok:
            return
        self.pointContainer.setEnabled(True)
        self.createCurveBtn.setEnabled(False)
        self.__currentCurve = Curve(value)
        self.drawBox.objectsList.append(self.__currentCurve)

    def addPoint(self):
        if self.__currentCurve is None:
            return
        self.__currentCurve.addPoint(Point(self.pointXSpin.value(), self.pointYSpin.value()))
        self.drawBox.update()

        if self.__currentCurve.isComplete():
            self.pointContainer.setEnabled(False)
            self.createCurveBtn.setEnabled(True)
            self.__currentCurve = None
