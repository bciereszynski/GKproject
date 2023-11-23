from PyQt5.QtGui import QImage, qRed, qRgb
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
        self.apply(0, "FIT")

    def apply(self, value, condition):
        shape: list[list] = [[1, 1, 0], [1, 0, 0], [1, 0, 0]]
        #shape: list[list] = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
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
