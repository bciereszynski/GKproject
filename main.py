import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QComboBox, QSpinBox, QPushButton

from shapes import Point


class Paint(QtWidgets.QWidget):
    def __init__(self, shapes, parent=None):
        super(Paint, self).__init__(parent)
        self.setBackgroundRole(QtGui.QPalette.Base)
        self.setAutoFillBackground(True)

        self.resize = False

        self._width = 350
        self._height = 250
        self._rect = QtCore.QRect(QtCore.QPoint(self.rect().center()), QtCore.QSize(self._width, self._height))
        self._initial_pos = QtCore.QPoint(self.rect().center())
        self.shapes = shapes


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
    def __init__(self, shapes, parent=None):
        super(Menu, self).__init__(parent)
        self.setBackgroundRole(QtGui.QPalette.Window)
        self.setAutoFillBackground(True)
        self.resize = False
        self.setFixedWidth(300)

        self.combobox = QComboBox()
        self.combobox.addItem("Linia")
        self.combobox.addItem("Prostokąt")
        self.combobox.addItem("Okrąg")

        self.spinPoint1 = QSpinBox()
        self.spinPoint2 = QSpinBox()

        self.createButton = QPushButton("Stwórz")
        self.createButton.clicked.connect(self.createShape)

        self.lay = QtWidgets.QVBoxLayout()
        self.lay.addWidget(self.combobox)
        self.lay.addWidget(self.spinPoint1)
        self.lay.addWidget(self.spinPoint2)
        self.lay.addWidget(self.createButton)
        self.setLayout(self.lay)
        self.shapes = shapes

    def createShape(self):
        self.shapes.append(Point(self.spinPoint1.value(), self.spinPoint2.value()))
        self.parent().paint.update()
        print(f"created {self.combobox.currentText()} {self.spinPoint1.value()} {self.spinPoint2.value()}")
class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setGeometry(QtCore.QRect(200, 100, 1200, 600))
        shapes = []
        self.paint = Paint(shapes)
        self.menu = Menu(shapes, self)
        self.sizeHint()
        self.lay = QtWidgets.QHBoxLayout()
        self.lay.addWidget(self.paint, stretch=2)
        self.lay.addWidget(self.menu, stretch=0)
        self.setLayout(self.lay)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())