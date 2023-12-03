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

        self.shapeEdit = QPlainTextEdit()
        self.shapeEdit.setFixedSize(61, 100)
        self.shapeEdit.setLineWrapMode(QPlainTextEdit.NoWrap)
        text = "1 1 1\n1 1 1\n1 1 1"
        self.shapeEdit.setPlainText(text)
        self.controlsLay.addWidget(self.shapeEdit)

    def mouseMoveEvent(self, e):
        super()
        p = self.shapeEdit.mapFromParent(e.pos())
        if p.x() > 60:
            self.shapeEdit.setFixedWidth(p.x())
        if p.y() > 100:
            self.shapeEdit.setFixedHeight(p.y())

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
        test = None
        while test != self.currentImage:
            test = self.currentImage
            self.apply(255,"FIT")

    def Thickening(self):
        test = None
        while test != self.currentImage:
            test = self.currentImage
            self.apply(0, "FIT")


    def apply(self, value, condition):
        shape = self.__parseShape()
        image = QImage(self.currentImage)
        shape_size = len(shape)
        reach = shape_size // 2

        for x in range(reach, image.width() - reach):
            for y in range(reach, image.height() - reach):
                result = self.hit_or_miss(x, y, shape)

                if result == condition:
                    image.setPixel(x, y, qRgb(value, value, value))


        self.updateImage(image)



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
