from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QComboBox, QSpinBox, QPushButton, QLabel

from shapes import Point
from PyQt5.QtCore import Qt


class ShapesMenu(QtWidgets.QWidget):
    # noinspection PyUnresolvedReferences
    def __init__(self, paint, parent=None):
        super(ShapesMenu, self).__init__(parent)
        self.setBackgroundRole(QtGui.QPalette.Window)
        self.setAutoFillBackground(True)
        self.resize = False
        self.setFixedWidth(300)
        self.setFixedHeight(400)
        self.paint = paint

        self.lay = QtWidgets.QVBoxLayout()

        self.shapeTypeCombo = QComboBox()
        self.shapeTypeCombo.addItem("Line")
        self.shapeTypeCombo.addItem("Rectangle")
        self.shapeTypeCombo.addItem("Circle")
        self.shapeTypeCombo.currentTextChanged.connect(self.paint.setShapeType)
        self.lay.addWidget(self.shapeTypeCombo)

        self.lay.addSpacing(50)

        self.point1WidthLabel = QLabel("Point A x:")
        self.point1WidthSpin = QSpinBox()
        self.point1WidthSpin.setMaximum(2000)
        self.lay.addWidget(self.point1WidthLabel)
        self.lay.addWidget(self.point1WidthSpin)

        self.point1HeightLabel = QLabel("Point A y:")
        self.point1HeightSpin = QSpinBox()
        self.point1HeightSpin.setMaximum(1000)
        self.lay.addWidget(self.point1HeightLabel)
        self.lay.addWidget(self.point1HeightSpin)

        self.point2WidthLabel = QLabel("Point B x:")
        self.point2WidthSpin = QSpinBox()
        self.point2WidthSpin.setMaximum(2000)
        self.lay.addWidget(self.point2WidthLabel)
        self.lay.addWidget(self.point2WidthSpin)

        self.point2HeightLabel = QLabel("Point B y:")
        self.point2HeightSpin = QSpinBox()
        self.point2HeightSpin.setMaximum(1000)
        self.lay.addWidget(self.point2HeightLabel)
        self.lay.addWidget(self.point2HeightSpin)

        self.createButton = QPushButton("Create")
        self.createButton.clicked.connect(self.createShape)
        self.createButton.setDefault(True)
        self.lay.addWidget(self.createButton)

        self.editButton = QPushButton("Edit")
        self.editButton.clicked.connect(self.editShape)
        self.editButton.setEnabled(False)
        self.lay.addWidget(self.editButton)

        self.deleteButton = QPushButton("Delete")
        self.deleteButton.clicked.connect(self.deleteShape)
        self.deleteButton.setEnabled(False)
        self.lay.addWidget(self.deleteButton)

        self.lay.setAlignment(Qt.AlignTop)
        self.setLayout(self.lay)

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

    def editSlot(self):
        self.editButton.setEnabled(True)
        self.editButton.setDefault(True)
        self.deleteButton.setEnabled(True)
        self.createButton.setEnabled(False)
        self.createButton.setDefault(False)
        self.shapeTypeCombo.setEnabled(False)
        point1 = self.paint.shapeSelected.point1
        point2 = self.paint.shapeSelected.point2
        self.point1HeightSpin.setValue(point1.y)
        self.point1WidthSpin.setValue(point1.x)
        self.point2HeightSpin.setValue(point2.y)
        self.point2WidthSpin.setValue(point2.x)

    def stopEditSlot(self):
        self.editButton.setEnabled(False)
        self.editButton.setDefault(False)
        self.deleteButton.setEnabled(False)
        self.createButton.setEnabled(True)
        self.createButton.setDefault(True)
        self.shapeTypeCombo.setEnabled(True)
