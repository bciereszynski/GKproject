import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QComboBox, QSpinBox, QPushButton, QLabel

from shapes import Point, Rectangle


class Paint(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Paint, self).__init__(parent)
        self.setBackgroundRole(QtGui.QPalette.Base)
        self.setAutoFillBackground(True)

        self.resize = False

        self._width = 350
        self._height = 250
        self._rect = QtCore.QRect(QtCore.QPoint(self.rect().center()), QtCore.QSize(self._width, self._height))
        self._initial_pos = QtCore.QPoint(self.rect().center())
        self.shapes = []


    def showEvent(self, event):
        super(Paint, self).showEvent(event)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setBrush(QtGui.QBrush( QtCore.Qt.cyan))
        painter.setPen(QtCore.Qt.darkCyan)
        for sh in self.shapes:
            sh.render(painter)
        painter.drawRect(self._rect)

    def mousePressEvent(self, event):
        if self._rect.contains(event.pos()):
            QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
            self.resize = True
            self._initial_pos = event.pos()
        super(Paint, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.resize == True:
            delta = event.pos() - self._initial_pos
            self._rect.setWidth(self._rect.width()+delta.x())
            self._rect.setHeight(self._rect.height()+delta.y())
            self.update()
            self._initial_pos = event.pos()
        super(Paint, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        QtWidgets.QApplication.restoreOverrideCursor()
        self.resize = False
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
        self.combobox.addItem("Linia")
        self.combobox.addItem("Prostokąt")
        self.combobox.addItem("Okrąg")

        self.spinPoint1Width = QSpinBox()
        self.spinPoint1Width.setMaximum(2000)
        self.spinPoint1Height = QSpinBox()
        self.spinPoint1Height.setMaximum(1000)

        self.spinPoint2Width = QSpinBox()
        self.spinPoint2Width.setMaximum(2000)
        self.spinPoint2Height = QSpinBox()
        self.spinPoint2Height.setMaximum(1000)

        self.createButton = QPushButton("Stwórz")
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