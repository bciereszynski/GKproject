from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QComboBox, QSpinBox, QPushButton, QLabel

from shapes import Point, Rectangle, Line, Circle
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
        self.lay.addWidget(self.shapeTypeCombo)

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

        self.lay.addWidget(self.createButton)
        self.lay.setAlignment(Qt.AlignTop)
        self.setLayout(self.lay)

    def createShape(self):
        point1 = Point(self.point1WidthSpin.value(), self.point1HeightSpin.value())
        point2 = Point(self.point2WidthSpin.value(), self.point2HeightSpin.value())
        if self.shapeTypeCombo.currentText() == "Line":
            self.paint.shapes.append(Line(point1, point2))
        elif self.shapeTypeCombo.currentText() == "Rectangle":
            self.paint.shapes.append(Rectangle(point1, point2))
        elif self.shapeTypeCombo.currentText() == "Circle":
            self.paint.shapes.append(Circle(point1, point2))
        self.paint.update()
