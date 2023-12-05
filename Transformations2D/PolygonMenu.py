from PyQt5.QtWidgets import QVBoxLayout, QWidget, QInputDialog

from Primitives.Menu import Menu
from Transformations2D.Polygon import Polygon
from Transformations2D.Vertex import Vertex


class PolygonMenu(Menu):
    def __init__(self, drawBox):
        super().__init__()

        self.drawBox = drawBox

        self.drawBox.completeSig = self.endCreate
        self.drawBox.editSig = self.updateEdit
        self.drawBox.stopEditSig = self.endEdit

        self.createPolygonBtn = self.createButton("Start making polygon", self.createPolygon)

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
        self.__currentPolygon = None

        self.translationBtn = self.createButton("Translation mode", self.setTranslation)
        self.rotateBtn = self.createButton("Rotation mode", self.setRotation)
        self.rotateBtn = self.createButton("Scale mode", self.setScale)

    def setTranslation(self):
        self.drawBox.mode = "trans"

    def setRotation(self):
        self.drawBox.mode = "rotate"

    def setScale(self):
        self.drawBox.mode = "scale"

    def updateSelectedPoint(self):
        point = self.drawBox.selectedObject
        if point is None:
            return
        point.setX(self.pointXSpin.value())
        point.setY(self.pointYSpin.value())
        self.drawBox.update()

    def createPolygon(self):
        (value, ok) = QInputDialog().getInt(self, "Polygon level", "Level:", 2, 2, 10)
        if not ok:
            return
        self.pointContainer.setEnabled(True)
        self.createPolygonBtn.setEnabled(False)
        self.__currentPolygon = Polygon(value)
        self.drawBox.objectsList.append(self.__currentPolygon)
        self.drawBox.mode = None

    def addPoint(self):
        if self.__currentPolygon is None:
            return
        self.__currentPolygon.addPoint(Vertex(self.pointXSpin.value(), self.pointYSpin.value()))

    def endEdit(self):
        self.pointContainer.setEnabled(False)
        self.createPolygonBtn.setEnabled(True)
        self.__currentPolygon = None

    def endCreate(self):
        self.endEdit()
        self.addPointBtn.setEnabled(False)

    def updateEdit(self):
        self.pointContainer.setEnabled(True)
