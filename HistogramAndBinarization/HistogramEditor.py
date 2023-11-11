from PyQt5.QtGui import QImage, qRed, qRgb
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QInputDialog

from ImageOperations.ImageEditor import ImageEditor


class HistogramEditor(ImageEditor):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.createControlButton("Stretch", self.stretch)
        self.createControlButton("Equalize", self.equalize)

        self.controlsLay.addSpacing(20)
        self.createControlButton("Binarize with value", self.binarizeWithValue)
        self.createControlButton("Binarize with percent", self.binarizeWithPercent)

    def createHistogram(self):
        histogram = [0] * 256
        image = QImage(self.currentImage)
        for x in range(image.width()):
            for y in range(image.height()):
                value = qRed(image.pixel(x, y))
                histogram[value] += 1
        return histogram

    def plotHistogram(self, histogram):
        x = [i for i in range(256)]
        plt.plot(x, histogram)
        plt.show()

    def equalize(self):
        image = QImage(self.currentImage)
        histogram = self.createHistogram()
        total = sum(histogram)

        LUT = [0] * 256
        LUT[0] = histogram[0]
        for i in range(1, 256):
            LUT[i] = LUT[i-1] + histogram[i]

        for x in range(image.width()):
            for y in range(image.height()):
                value = qRed(image.pixel(x, y))
                newValue = LUT[value] / total
                newValue = int(newValue*255)
                image.setPixel(x, y, qRgb(newValue, newValue, newValue))
        self.updateImage(image)

    def stretch(self):
        self.toGrayscaleLinear()
        image = QImage(self.currentImage)
        valueMin = 255
        valueMax = 0
        for x in range(image.width()):
            for y in range(image.height()):
                # after convertion to grayscale: r == g == b
                value = qRed(image.pixel(x, y))
                valueMin = min(value, valueMin)
                valueMax = max(value, valueMax)

        valueDiff = valueMax - valueMin
        for x in range(image.width()):
            for y in range(image.height()):
                value = qRed(image.pixel(x, y))
                newValue = int((value - valueMin) / valueDiff * 255)
                image.setPixel(x, y, qRgb(newValue, newValue, newValue))
        self.updateImage(image)

    def binarizeWithValue(self):
        (value, ok) = QInputDialog().getInt(self, "Threshold", "Threshold value:", 100, 0, 255)
        if not ok:
            return
        self.binarize(value)

    def binarizeWithPercent(self):
        (percent, ok) = QInputDialog().getInt(self, "Threshold", "Threshold percent:", 50, 0, 100)
        if not ok:
            return

        histogram = self.createHistogram()
        desiredValue = sum(histogram) * (percent/100)
        threshold = -1
        accum = 0

        while accum < desiredValue:
            threshold += 1
            accum += histogram[threshold]

        self.binarize(threshold)

    def binarize(self, threshold):
        self.toGrayscaleLinear()
        image = QImage(self.currentImage)

        LUT = [0] * 256
        for i in range(256):
            LUT[i] = 0 if i < threshold else 255

        for x in range(image.width()):
            for y in range(image.height()):
                value = qRed(image.pixel(x, y))
                newValue = LUT[value]
                image.setPixel(x, y, qRgb(newValue, newValue, newValue))
        self.updateImage(image)
