from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QSpinBox, QPushButton


class Menu(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setBackgroundRole(QtGui.QPalette.Window)
        self.setAutoFillBackground(True)
        self.resize = False
        self.setFixedWidth(300)

        self.lay = QtWidgets.QVBoxLayout()
        self.setLayout(self.lay)

        self.lay.setAlignment(Qt.AlignTop)

    def createSpinBox(self, name, maximum, autoAdd=True):
        label = QLabel(name)
        spin = QSpinBox()
        spin.setMaximum(maximum)
        spin.setMinimum(0)
        if autoAdd:
            self.lay.addWidget(label)
            self.lay.addWidget(spin)
        return spin, label

    def createButton(self, name, action, autoAdd=True):
        button = QPushButton(name)
        button.clicked.connect(action)
        if autoAdd:
            self.lay.addWidget(button)
        return button
