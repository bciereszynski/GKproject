from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QComboBox, QSpinBox, QPushButton

from shapes import Point, Rectangle, Line, Circle


class Menu(QtWidgets.QWidget):
    def __init__(self, paint, parent = None):
        super(Menu, self).__init__(parent)
        self.setBackgroundRole(QtGui.QPalette.Window)
        self.setAutoFillBackground(True)
        self.resize = False
        self.setFixedWidth(300)
        self.paint = paint

        self.combobox = QComboBox()
        self.combobox.addItem("Line")
        self.combobox.addItem("Rectangle")
        self.combobox.addItem("Circle")

        self.spinPoint1Width = QSpinBox()
        self.spinPoint1Width.setMaximum(2000)
        self.spinPoint1Height = QSpinBox()
        self.spinPoint1Height.setMaximum(1000)

        self.spinPoint2Width = QSpinBox()
        self.spinPoint2Width.setMaximum(2000)
        self.spinPoint2Height = QSpinBox()
        self.spinPoint2Height.setMaximum(1000)

        self.createButton = QPushButton("Create")
        self.createButton.clicked.connect(self.createShape)

        self.lay = QtWidgets.QVBoxLayout()
        self.lay.addWidget(self.combobox)
        self.lay.addWidget(self.spinPoint1Width)
        self.lay.addWidget(self.spinPoint1Height)
        self.lay.addWidget(self.spinPoint2Width)
        self.lay.addWidget(self.spinPoint2Height)
        self.lay.addWidget(self.createButton)
        self.setLayout(self.lay)

    def createShape(self):
        point1 = Point(self.spinPoint1Width.value(), self.spinPoint1Height.value())
        point2 = Point(self.spinPoint2Width.value(), self.spinPoint2Height.value())
        if self.combobox.currentText() == "Line":
            self.paint.shapes.append(Line(point1, point2))
        elif self.combobox.currentText() == "Rectangle":
            self.paint.shapes.append(Rectangle(point1, point2))
        elif self.combobox.currentText() == "Circle":
            self.paint.shapes.append(Circle(point1, point2))
        self.paint.update()

