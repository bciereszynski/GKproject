from PyQt5.QtWidgets import QComboBox, QSpinBox, QPushButton, QLabel

from Point import Point
from Primitives.Menu import Menu


class ShapesMenu(Menu):
    def __init__(self, paint, parent=None):
        super().__init__(parent)
        self.paint = paint

        self.shapeTypeCombo = QComboBox()
        self.shapeTypeCombo.addItem("Line")
        self.shapeTypeCombo.addItem("Rectangle")
        self.shapeTypeCombo.addItem("Circle")
        self.shapeTypeCombo.currentTextChanged.connect(self.paint.setShapeType)
        self.lay.addWidget(self.shapeTypeCombo)

        self.lay.addSpacing(50)

        self.point1WidthSpin = self.createSpinBox("Point A x:", 2000)
        self.point1HeightSpin = self.createSpinBox("Point A y:", 1000)

        self.point2WidthSpin = self.createSpinBox("Point B x:", 2000)
        self.point2HeightSpin = self.createSpinBox("Point B y:", 1000)

        self.createBtn = self.createButton("Create", self.createShape)
        self.createBtn.setDefault(True)
        self.editBtn = self.createButton("Edit", self.editShape)
        self.editBtn.setEnabled(False)

        self.deleteBtn = self.createButton("Delete", self.deleteShape)
        self.deleteBtn.setEnabled(False)

    def createShape(self):
        point1 = Point(self.point1WidthSpin.value(), self.point1HeightSpin.value())
        point2 = Point(self.point2WidthSpin.value(), self.point2HeightSpin.value())
        self.paint.createShape(point1, point2)

    def editShape(self):
        point1 = Point(self.point1WidthSpin.value(), self.point1HeightSpin.value())
        point2 = Point(self.point2WidthSpin.value(), self.point2HeightSpin.value())
        self.paint.editShape(point1, point2)

    def deleteShape(self):
        self.paint.deleteShape()

    def EditState(self):
        self.editBtn.setEnabled(True)
        self.editBtn.setDefault(True)
        self.deleteBtn.setEnabled(True)
        self.createBtn.setEnabled(False)
        self.createBtn.setDefault(False)
        self.shapeTypeCombo.setEnabled(False)
        point1 = self.paint.objectSelected.point1
        point2 = self.paint.objectSelected.point2
        self.point1HeightSpin.setValue(point1.y)
        self.point1WidthSpin.setValue(point1.x)
        self.point2HeightSpin.setValue(point2.y)
        self.point2WidthSpin.setValue(point2.x)

    def NotEditState(self):
        self.editBtn.setEnabled(False)
        self.editBtn.setDefault(False)
        self.deleteBtn.setEnabled(False)
        self.createBtn.setEnabled(True)
        self.createBtn.setDefault(True)
        self.shapeTypeCombo.setEnabled(True)
