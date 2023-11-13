from PyQt5.QtWidgets import QVBoxLayout, QWidget, QInputDialog

from BézierCurve.Curve import Curve
from Point import Point
from Primitives.Menu import Menu


class CurveMenu(Menu):
    def __init__(self, drawBox):
        super().__init__()

        self.drawBox = drawBox

        self.drawBox.completeSig = self.endCreate
        self.drawBox.editSig = self.updateEdit
        self.drawBox.stopEditSig = self.endEdit

        self.createCurveBtn = self.createButton("Start making curve", self.createCurve)

        self.pointContainer = QWidget()
        pointLay = QVBoxLayout(self.pointContainer)
        self.pointXSpin, label = self.createSpinBox("Point x:", 2000, autoAdd=False)
        self.pointXSpin.valueChanged.connect(self.updateSelectedPoint)
        pointLay.addWidget(label)
        pointLay.addWidget(self.pointXSpin)
        self.pointYSpin, label = self.createSpinBox("Point y:", 1000, autoAdd=False)
        self.pointYSpin.valueChanged.connect(self.updateSelectedPoint)
        pointLay.addWidget(label)
        pointLay.addWidget(self.pointYSpin)

        self.lay.addWidget(self.pointContainer)
        self.pointContainer.setEnabled(False)

        self.addPointBtn = self.createButton("Add point", self.addPoint)
        self.__currentCurve = None

    def updateSelectedPoint(self):
        point = self.drawBox.selectedObject
        if point is None:
            return
        point.setX(self.pointXSpin.value())
        point.setY(self.pointYSpin.value())
        self.drawBox.update()

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

    def endEdit(self):
        self.pointContainer.setEnabled(False)
        self.createCurveBtn.setEnabled(True)
        self.__currentCurve = None

    def endCreate(self):
        self.endEdit()
        self.addPointBtn.setEnabled(False)

    def updateEdit(self):
        self.pointContainer.setEnabled(True)
        self.pointXSpin.blockSignals(True)
        self.pointYSpin.blockSignals(True)
        self.pointXSpin.setValue(self.drawBox.selectedObject.x)
        self.pointYSpin.setValue(self.drawBox.selectedObject.y)
        self.pointXSpin.blockSignals(False)
        self.pointYSpin.blockSignals(False)
