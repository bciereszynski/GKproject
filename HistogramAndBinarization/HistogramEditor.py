from PyQt5.QtGui import QImage, qRed, qRgb
import matplotlib.pyplot as plt

from ImageOperations.ImageEditor import ImageEditor


class HistogramEditor(ImageEditor):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.createControlButton("Stretch", self.stretch)
        self.createControlButton("Equalize", self.equalize)

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
