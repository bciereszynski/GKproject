from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage, qBlue, qRed, qRgb, qGreen
from PyQt5.QtWidgets import QSpinBox, QLabel, QHBoxLayout, QPushButton, QFileDialog, QInputDialog, QPlainTextEdit, QCheckBox

from ImageOperations.ImageEditor import ImageEditor


class PixelEditor(ImageEditor):
    def __init__(self, parent=None):
        super(PixelEditor, self).__init__(parent)

        self.createControlButton("Grayscale - average", self.toGrayscaleAvg)
        self.createControlButton("Grayscale - linear", self.toGrayscaleLinear)

        self.comboLay = QHBoxLayout()

        self.redCheckCombo, redCheckLabel = self.__createControlCheck("Red")
        self.greenCheckCombo, greenCheckLabel = self.__createControlCheck("Green")
        self.blueCheckCombo, blueCheckLabel = self.__createControlCheck("Blue")

        self.controlsLay.addLayout(self.comboLay)
        self.controlsLay.setAlignment(self.comboLay, Qt.AlignTop)

        self.controlsLay.addSpacing(20)

        self.spin = QSpinBox()
        self.spin.setMaximum(255)
        self.spin.setMinimum(0)
        self.controlsLay.addWidget(self.spin)
        self.createControlButton("Add", self.add)
        self.createControlButton("Subtract", self.subtract)
        self.createControlButton("Multiply", self.multiply)
        self.createControlButton("Divide", self.divide)

        self.controlsLay.addSpacing(20)

        self.createControlButton("Average", self.setAvgMask)
        self.createControlButton("Sobel", self.setSobel)
        self.createControlButton("Sharp", self.setSharp)
        self.createControlButton("Gauss", self.setGauss)

        self.maskEdit = QPlainTextEdit()
        self.maskEdit.setFixedSize(61, 100)
        self.maskEdit.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.controlsLay.addWidget(self.maskEdit)

        self.createControlButton("Median", self.medianFilter)
        self.createControlButton("Apply mask", self.applyMask)

    def __createControlCheck(self, name):
        check = QCheckBox()
        check.setChecked(True)
        label = QLabel(name)
        lay = QHBoxLayout()
        lay.addWidget(check)
        lay.addWidget(label)
        self.comboLay.addLayout(lay)
        return check, label

    def setAvgMask(self):
        text = "1 1 1\n1 1 1\n1 1 1"
        self.maskEdit.setPlainText(text)

    def setSobel(self):
        text = "1 0 -1\n2 0 -2\n1 0 -1"
        self.maskEdit.setPlainText(text)

    def setSharp(self):
        text = "0 -1 0\n-1 5 -1\n0 -1 0"
        self.maskEdit.setPlainText(text)

    def setGauss(self):
        text = "1 4 6 4 1\n4 16 24 16 4\n6 24 36 24 6\n4 16 24 16 4\n1 4 6 4 1"
        self.maskEdit.setPlainText(text)

    def mouseMoveEvent(self, e):
        super()
        p = self.maskEdit.mapFromParent(e.pos())
        if p.x() > 60:
            self.maskEdit.setFixedWidth(p.x())
        if p.y() > 100:
            self.maskEdit.setFixedHeight(p.y())

    def toGrayscaleAvg(self):
        image = QImage(self.currentImage)
        for x in range(image.width()):
            for y in range(image.height()):
                rgb = image.pixel(x, y)
                r = qRed(rgb)
                g = qGreen(rgb)
                b = qBlue(rgb)
                gray = (r + g + b) // 3
                rgb = qRgb(gray, gray, gray)
                image.setPixel(x, y, rgb)
        self.updateImage(image)

    def add(self):
        value = self.spin.value()
        self.modifyPixels(lambda x, y: x + y, value,
                          [self.redCheckCombo.isChecked(), self.greenCheckCombo.isChecked(),
                           self.blueCheckCombo.isChecked()])

    def subtract(self):
        value = self.spin.value()
        self.modifyPixels(lambda x, y: x - y, value,
                          [self.redCheckCombo.isChecked(), self.greenCheckCombo.isChecked(),
                           self.blueCheckCombo.isChecked()])

    def multiply(self):
        value = self.spin.value()
        self.modifyPixels(lambda x, y: x * y, value,
                          [self.redCheckCombo.isChecked(), self.greenCheckCombo.isChecked(),
                           self.blueCheckCombo.isChecked()])

    def divide(self):
        value = self.spin.value()
        if value == 0:
            print("error")
            return
        self.modifyPixels(lambda x, y: int(x / y), value,
                          [self.redCheckCombo.isChecked(), self.greenCheckCombo.isChecked(),
                           self.blueCheckCombo.isChecked()])

    def applyMask(self):
        try:
            mask = self.__parseMask()
        except Exception as ex:
            print(str(ex))
            return
        self.__maskImage(mask,
                         [self.redCheckCombo.isChecked(), self.greenCheckCombo.isChecked(),
                          self.blueCheckCombo.isChecked()])

    def modifyPixels(self, operation, value, channels):
        image = QImage(self.currentImage)
        for x in range(image.width()):
            for y in range(image.height()):
                rgb = image.pixel(x, y)
                r = qRed(rgb) if not channels[0] else self.limitPixel(operation(qRed(rgb), value))
                g = qGreen(rgb) if not channels[1] else self.limitPixel(operation(qGreen(rgb), value))
                b = qBlue(rgb) if not channels[2] else self.limitPixel(operation(qBlue(rgb), value))
                newRgb = qRgb(r, g, b)
                image.setPixel(x, y, newRgb)
        self.updateImage(image)

    def medianFilter(self):
        channels = [self.redCheckCombo.isChecked(), self.greenCheckCombo.isChecked(),
                          self.blueCheckCombo.isChecked()]
        image = QImage(self.currentImage)
        mask_size = 3
        reach = mask_size // 2
        for x in range(reach, image.width() - reach):
            for y in range(reach, image.height() - reach):
                rList = []
                gList = []
                bList = []
                for i in range(mask_size):
                    for j in range(mask_size):
                        oldRgb = self.currentImage.pixel(x + i - reach, y + j - reach)
                        rList.append(qRed(oldRgb))
                        gList.append(qGreen(oldRgb))
                        bList.append(qBlue(oldRgb))
                rList.sort()
                gList.sort()
                bList.sort()
                rgb = self.currentImage.pixel(x, y)
                r = qRed(rgb) if not channels[0] else rList[4]
                g = qGreen(rgb) if not channels[1] else gList[4]
                b = qBlue(rgb) if not channels[2] else bList[4]
                newRgb = qRgb(r, g, b)
                image.setPixel(x, y, newRgb)
        self.updateImage(image)

    def __maskImage(self, mask: list[list], channels):
        image = QImage(self.currentImage)
        mask_size = len(mask)
        count = 0
        for row in mask:
            for item in row:
                count = count + item

        if count == 0:
            count = 1
        reach = mask_size // 2
        for x in range(reach, image.width() - reach):
            for y in range(reach, image.height() - reach):
                r = 0
                g = 0
                b = 0
                for i in range(mask_size):
                    for j in range(mask_size):
                        oldRgb = self.currentImage.pixel(x + i - reach, y + j - reach)
                        r = r + qRed(oldRgb) * mask[i][j]
                        g = g + qGreen(oldRgb) * mask[i][j]
                        b = b + qBlue(oldRgb) * mask[i][j]
                rgb = self.currentImage.pixel(x, y)
                r = qRed(rgb) if not channels[0] else self.limitPixel(r / count)
                g = qGreen(rgb) if not channels[1] else self.limitPixel(g / count)
                b = qBlue(rgb) if not channels[2] else self.limitPixel(b / count)
                newRgb = qRgb(r, g, b)
                image.setPixel(x, y, newRgb)
        self.updateImage(image)

    def __parseMask(self):
        lines = self.maskEdit.toPlainText().splitlines()
        mask = []
        mask_size = len(lines)
        if mask_size % 2 != 1:
            raise Exception("Mask size must be odd")
        for line in lines:
            mask_line = []
            for item in line.split():
                try:
                    int(item)
                except ValueError:
                    raise Exception("Not numeric item occurred")
                mask_line.append(int(item))
            if mask_size != len(mask_line):
                raise Exception("Mask not fully filled")
            mask.append(mask_line)
        return mask
