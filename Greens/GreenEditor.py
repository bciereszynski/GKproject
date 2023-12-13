from time import sleep

from PyQt5.QtGui import QImage, qGreen, qRgb, qBlue, qRed
from PyQt5.QtWidgets import QInputDialog, QLabel

from ImageOperations.ImageEditor import ImageEditor


class GreenEditor(ImageEditor):

    def __init__(self):
        super().__init__()
        self.createControlButton("Remove red/blue", self.removeRedAndBlue)
        self.createControlButton("Binarize", self.binarize)
        self.createControlButton("Closure", self.Closure)
        self.createControlButton("Opening", self.Opening)
        self.createControlButton("Calculate percent", self.countPercent)

        self.percentLabel = QLabel("...")
        self.controlsLay.addWidget(self.percentLabel)

    def removeRedAndBlue(self):
        (value, ok) = QInputDialog().getInt(self, "Threshold", "Threshold value:", 122, 0, 255)
        if not ok:
            return
        image = QImage(self.currentImage)
        for x in range(image.width()):
            for y in range(image.height()):
                rgb = image.pixel(x, y)
                r = qRed(rgb)
                g = qGreen(rgb)
                b = qBlue(rgb)
                if b + r > value*2:
                    gray = 0
                else:
                    gray = g
                rgb = qRgb(0, gray, 0)
                image.setPixel(x, y, rgb)
        self.updateImage2(image)

    def binarize(self):
        (value, ok) = QInputDialog().getInt(self, "Threshold", "Threshold value:", 67, 0, 255)
        if not ok:
            return
        self.__binarize(value)

    def __binarize(self, threshold):
        image = QImage(self.currentImage)

        LUT = [0] * 256
        for i in range(256):
            LUT[i] = 0 if i > threshold else 255

        for x in range(image.width()):
            for y in range(image.height()):
                value = qGreen(image.pixel(x, y))
                newValue = LUT[value]
                image.setPixel(x, y, qRgb(newValue, newValue, newValue))
        self.updateImage2(image)

    def Opening(self):
        self.Erosion()
        self.Dilation()

    def Closure(self):
        self.Dilation()
        self.Erosion()

    def Erosion(self):
        self.apply(255, "HIT")

    def Dilation(self):
        self.apply(0, "HIT")

    def apply(self, value, condition):
        shape = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
        image = QImage(self.currentImage)
        shape_size = len(shape)
        reach = shape_size // 2
        pixels = []

        for x in range(reach, image.width() - reach):
            for y in range(reach, image.height() - reach):
                if image.pixelColor(x, y).red() == value:
                    continue
                result = self.hit_or_miss(x, y, shape)
                if result == condition:
                    image.setPixel(x, y, qRgb(value, value, value))
                    pixels.append((x, y))

        self.updateImage2(image)
        return pixels

    def hit_or_miss(self, x, y, shape):
        shape_size = len(shape)
        reach = shape_size // 2
        count = 0
        for row in shape:
            for item in row:
                count = count + item

        coverage = 0
        for i in range(shape_size):
            for j in range(shape_size):
                oldRgb = self.currentImage.pixel(x + i - reach, y + j - reach)
                value = 1 if qRed(oldRgb) < 127 else 0
                if value == shape[i][j] == 1:
                    coverage += 1
        if coverage == count:
            return "FIT"
        elif coverage == 0:
            return "MISS"
        else:
            return "HIT"

    def countPercent(self):
        count = 0
        count_obj = 0
        image = QImage(self.currentImage)
        for x in range(image.width()):
            for y in range(image.height()):
                rgb = image.pixel(x, y)
                value = qGreen(rgb)
                if value == 0:
                    count_obj += 1
                count += 1
        self.percentLabel.setText(str(count_obj/count))

    def updateImage2(self, image):
        sleep(2)
        self.updateImage(image)
