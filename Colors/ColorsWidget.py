from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QSlider

from Colors.TextSlider import TextSlider


class ColorsWidget(QWidget):
    def __init__(self, parent=None):
        super(ColorsWidget, self).__init__(parent)

        self.lay = QHBoxLayout()
        self.setLayout(self.lay)

        self.rgbLay = QVBoxLayout()
        self.lay.addLayout(self.rgbLay)
        self.rgbLabel = QLabel("RGB")
        self.rgbLay.addWidget(self.rgbLabel)
        self.rgbLay.setAlignment(Qt.AlignTop)

        self.rSlider = self.__createSlider(self.rgbLay, "r", self.updateCMYK)
        self.gSlider = self.__createSlider(self.rgbLay, "g", self.updateCMYK)
        self.bSlider = self.__createSlider(self.rgbLay, "b", self.updateCMYK)

        self.cmykLay = QVBoxLayout()
        self.lay.addLayout(self.cmykLay)
        self.cmykLabel = QLabel("CMYK")
        self.cmykLay.setAlignment(Qt.AlignTop)
        self.cmykLay.addWidget(self.cmykLabel)

        self.cSlider = self.__createSlider(self.cmykLay, "c", self.updateRGB)
        self.mSlider = self.__createSlider(self.cmykLay, "m", self.updateRGB)
        self.ySlider = self.__createSlider(self.cmykLay, "y", self.updateRGB)
        self.kSlider = self.__createSlider(self.cmykLay, "k", self.updateRGB)

        self.colorLabel = QLabel()
        self.colorLabel.setFixedSize(100, 300)
        self.colorLabel.setStyleSheet("QLabel{background-color:rgb(0,0,0);border:2px solid black;}")
        self.lay.addWidget(self.colorLabel)

        self.updateCMYK()

    def __createSlider(self, lay, name, command):
        slider = TextSlider(name)
        slider.setMinimum(0)
        slider.setMaximum(255)
        slider.valueChanged.connect(command)
        lay.addWidget(slider)
        return slider

    def updateRGB(self):
        c = self.cSlider.value() / 255
        m = self.mSlider.value() / 255
        y = self.ySlider.value() / 255
        k = self.kSlider.value() / 255
        r = (1 - min(1, c * (1 - k) + k)) * 255
        g = (1 - min(1, m * (1 - k) + k)) * 255
        b = (1 - min(1, y * (1 - k) + k)) * 255
        self.__setSliderValueSilent(self.rSlider, r)
        self.__setSliderValueSilent(self.gSlider, g)
        self.__setSliderValueSilent(self.bSlider, b)

        self.updateColor(r, g, b)

    def updateCMYK(self):
        r = self.rSlider.value() / 255
        g = self.gSlider.value() / 255
        b = self.bSlider.value() / 255
        k = min(1 - r, 1 - g, 1 - b)

        if k == 1:
            c, m, y = 255, 255, 255
        else:
            c = (1 - r - k) / (1 - k) * 255
            m = (1 - g - k) / (1 - k) * 255
            y = (1 - b - k) / (1 - k) * 255

        self.__setSliderValueSilent(self.cSlider, c)
        self.__setSliderValueSilent(self.mSlider, m)
        self.__setSliderValueSilent(self.ySlider, y)
        self.__setSliderValueSilent(self.kSlider, k * 255)

        self.updateColor(r * 255, g * 255, b * 255)

    def updateColor(self, r, g, b):
        self.colorLabel.setStyleSheet(
            "QLabel{background-color:rgb(" + str(int(r)) + "," + str(int(g)) + "," + str(int(b)) + ");}")

    @staticmethod
    def __setSliderValueSilent(slider, value):
        slider.blockSignals(True)
        slider.setValue(int(value))
        slider.blockSignals(False)
