import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QComboBox, QSpinBox, QPushButton, QLabel

from shapes import Point, Rectangle, Line


class Paint(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Paint, self).__init__(parent)
        self.setBackgroundRole(QtGui.QPalette.Base)
        self.setAutoFillBackground(True)
        self.setMouseTracking(True)

        self.shapes = []

        self._objectToMove = None
        self._objectToResize = None
        self._initial_pos = None

    def showEvent(self, event):
        super(Paint, self).showEvent(event)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setBrush(QtGui.QBrush( QtCore.Qt.cyan))
        painter.setPen(QtCore.Qt.darkCyan)
        for sh in self.shapes:
            sh.render(painter)

    def mousePressEvent(self, event):
        for sh in self.shapes:
            if sh.checkResize(event.pos()):
                self._objectToResize = sh
                self._initial_pos = event.pos()
            elif sh.checkMove(event.pos()):
                self._objectToMove = sh
                self._initial_pos = event.pos()

        super(Paint, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._objectToResize is not None:
            delta = event.pos() - self._initial_pos
            self._objectToResize.resize(delta)
            self.update()
            self._initial_pos = event.pos()
            return
        if self._objectToMove is not None:
            delta = event.pos() - self._initial_pos
            self._objectToMove.move(delta)
            self.update()
            self._initial_pos = event.pos()
            return
        #else
        for sh in self.shapes:
            if sh.checkMove(event.pos()):
                self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
                return
            if sh.checkResize(event.pos()):
                self.setCursor(QtGui.QCursor(QtCore.Qt.SizeAllCursor))
                return
            self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        super(Paint, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self._objectToResize = None
        self._objectToMove = None
        super(Paint, self).mouseReleaseEvent(event)

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
        if self.combobox.currentText()=="Line":
            self.paint.shapes.append(Line(point1, point2))
        elif self.combobox.currentText()=="Rectangle":
            self.paint.shapes.append(Rectangle(point1, point2))
        self.paint.update()
class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setGeometry(QtCore.QRect(200, 100, 1200, 600))
        self.sizeLabel = QLabel()
        self.sizeLabel.setFixedSize(150,50)
        self.paint = Paint()
        self.menu = Menu(self.paint)
        self.sizeHint()
        self.lay = QtWidgets.QHBoxLayout()
        self.lay.addWidget(self.paint, stretch=2)
        self.lay.addWidget(self.menu, stretch=0)
        self.lay.addWidget(self.sizeLabel, stretch=0)
        self.setLayout(self.lay)

    def resizeEvent(self, a0):
        self.sizeLabel.setText(f"Field size: {self.paint.width()}, {self.paint.height()}")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())