from PyQt5.QtGui import QImage, qRed, qRgb
from PyQt5.QtWidgets import QPlainTextEdit

from ImageOperations.ImageEditor import ImageEditor

# https://homepages.inf.ed.ac.uk/rbf/HIPR2/morops.htm
#
# https://pl.wikipedia.org/wiki/Cyfrowe_przetwarzanie_obraz%C3%B3w_binarnych


class MorphologyEditor(ImageEditor):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.createControlButton("Erosion", self.Erosion)
        self.createControlButton("Dilation", self.Dilation)
        self.createControlButton("Opening", self.Opening)
        self.createControlButton("Closure", self.Closure)

        self.createControlButton("Thinning", self.Thinning)
        self.createControlButton("Thickening", self.Thickening)

        self.createControlButton("Hit or miss", self.Hitting)

        self.shapeEdit = QPlainTextEdit()
        self.shapeEdit.setFixedSize(61, 100)
        self.shapeEdit.setLineWrapMode(QPlainTextEdit.NoWrap)
        text = "1 1 1\n1 1 1\n1 1 1"
        self.shapeEdit.setPlainText(text)
        self.controlsLay.addWidget(self.shapeEdit)

        self.createControlButton("Rotate", self.rotateShape)

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

    def Thinning(self):
        test = self.currentImage
        pixels = self.apply(255, "FIT")
        shape = self.__parseShape()
        while test != self.currentImage:
            test = self.currentImage
            pixels = self.__applyOnlyChanged(255, "FIT", shape, pixels)

    def Thickening(self):
        test = self.currentImage
        pixels = self.apply(0, "FIT")
        shape = self.__parseShape()
        while test != self.currentImage:
            test = self.currentImage
            pixels = self.__applyOnlyChanged(0, "FIT", shape, pixels)

    def apply(self, value, condition):
        shape = self.__parseShape()
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

        self.updateImage(image)
        return pixels

    def __applyOnlyChanged(self, value, condition, shape, changedPixels):
        image = QImage(self.currentImage)
        shape_size = len(shape)
        reach = shape_size // 2
        pixels = []

        for a, b in changedPixels:
            for x in range(a - reach, a + reach + 1):
                for y in range(b - reach, b + reach + 1):
                    if image.pixelColor(x, y).red() == value:
                        continue
                    result = self.hit_or_miss(x, y, shape)
                    if result == condition:
                        image.setPixel(x, y, qRgb(value, value, value))
                        pixels.append((x, y))

        self.updateImage(image)
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

    def Hitting(self):
        shape = self.__parseShape()
        image = QImage(self.currentImage)
        shape_size = len(shape)
        reach = shape_size // 2

        for x in range(reach, image.width() - reach):
            for y in range(reach, image.height() - reach):
                result = self.hit_or_miss(x, y, shape)
                if result == "HIT":
                    image.setPixel(x, y, qRgb(0, 0, 0))
                elif result == "FIT":
                    image.setPixel(x, y, qRgb(127, 127, 127))
                else:
                    image.setPixel(x, y, qRgb(255, 255, 255))

        self.updateImage(image)

    def mouseMoveEvent(self, e):
        super()
        p = self.shapeEdit.mapFromParent(e.pos())
        if p.x() > 60:
            self.shapeEdit.setFixedWidth(p.x())
        if p.y() > 100:
            self.shapeEdit.setFixedHeight(p.y())

    def rotateShape(self):
        shape = self.__parseShape()
        shape = self.rotateArray(shape)
        text = ""
        for line in shape:
            for number in line:
                text += str(number) + " "
            text = text[:-1]
            text += '\n'
        text = text[:-1]
        self.shapeEdit.setPlainText(text)

    def __parseShape(self):
        lines = self.shapeEdit.toPlainText().splitlines()
        shape = []
        shape_size = len(lines)
        if shape_size % 2 != 1:
            raise Exception("shape size must be odd")
        for line in lines:
            shape_line = []
            for item in line.split():
                try:
                    int(item)
                except ValueError:
                    raise Exception("Not numeric item occurred")
                shape_line.append(int(item))
            if shape_size != len(shape_line):
                raise Exception("shape not fully filled")
            shape.append(shape_line)
        return shape

    @staticmethod
    def rotateArray(array):
        list_of_tuples = zip(*array[::-1])
        return list([list(elem) for elem in list_of_tuples])
