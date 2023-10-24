from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QSlider, QSpinBox


class TextSlider(QWidget):
    valueChanged = pyqtSignal(int)

    def __init__(self, name, orientation=Qt.Orientation.Horizontal, parent=None):
        super(TextSlider, self).__init__(parent)

        self.lay = QHBoxLayout()
        self.setLayout(self.lay)

        self.label = QLabel(name)
        self.lay.addWidget(self.label)

        self.slider = QSlider(orientation)
        self.lay.addWidget(self.slider)

        self.spinBox = QSpinBox()
        self.lay.addWidget(self.spinBox)
        self.spinBox.valueChanged.connect(self.slider.setValue)
        self.slider.valueChanged.connect(self.spinBox.setValue)

        self.slider.valueChanged.connect(self.emitValueChanged)

    def emitValueChanged(self, value):
        self.valueChanged.emit(value)

    def setMinimum(self, value):
        self.slider.setMinimum(value)
        self.spinBox.setMinimum(value)

    def setMaximum(self, value):
        self.slider.setMaximum(value)
        self.spinBox.setMaximum(value)

    def value(self):
        return self.slider.value()

    def setValue(self, value):
        self.slider.setValue(value)
        self.spinBox.setValue(value)

    def blockSignals(self, on):
        self.slider.blockSignals(on)
        self.spinBox.blockSignals(on)
