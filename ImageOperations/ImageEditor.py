from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage, qBlue, qRed, qRgb, qGreen
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QSpinBox, QLabel, \
    QHBoxLayout, QPushButton, QSlider, QFileDialog, QInputDialog, QPlainTextEdit


class ImageEditor(QWidget):
    def __init__(self, parent=None):
        super(ImageEditor, self).__init__(parent)
        self.lay = QHBoxLayout()
        self.setLayout(self.lay)

        self.originalImage = None

        self.imageLayout = QVBoxLayout()
        self.view = self.view = QGraphicsView(self)
        self.scene = QGraphicsScene(self)
        self.view.setScene(self.scene)
        self.pixmap_item = QGraphicsPixmapItem()
        self.scene.addItem(self.pixmap_item)

        self.saveFileButton = QPushButton("Save image file")
        self.saveFileButton.clicked.connect(self.saveBtnCommand)
        self.lay.setAlignment(self.saveFileButton, Qt.AlignTop)
        self.imageLayout.addWidget(self.saveFileButton)
        self.imageLayout.addWidget(self.view)

        self.lay.addLayout(self.imageLayout)

        self.controlsLay = QVBoxLayout()
        self.controlsLay.setAlignment(Qt.AlignTop)

        self.spin = QSpinBox()
        self.spin.setMaximum(255)
        self.spin.setMinimum(0)
        self.controlsLay.addWidget(self.spin)
        self.__createControlButton("Add", self.add)
        self.__createControlButton("Subtract", self.subtract)
        self.__createControlButton("Multiply", self.multiply)
        self.__createControlButton("Divide", self.divide)

        self.controlsLay.addSpacing(20)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMaximum(100)
        self.slider.setMinimum(0)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.controlsLay.addWidget(self.slider)
        self.__createControlButton("Change image brightness", self.changeBrightness)

        self.maskEdit = QPlainTextEdit()
        self.maskEdit.setFixedSize(61, 100)
        self.maskEdit.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.controlsLay.addWidget(self.maskEdit)

        self.applyMaskBtn = QPushButton("Apply mask")
        self.applyMaskBtn.clicked.connect(self.applyMask)
        self.controlsLay.addWidget(self.applyMaskBtn)

        self.lay.addLayout(self.controlsLay)

    def mouseMoveEvent(self, e):
        super()
        p = self.maskEdit.mapFromParent(e.pos())
        if p.x() > 60:
            self.maskEdit.setFixedWidth(p.x())
        if p.y() > 100:
            self.maskEdit.setFixedHeight(p.y())

    def __createControlButton(self, name, action):
        btn = QPushButton(name)
        btn.clicked.connect(action)
        self.controlsLay.addWidget(btn)
        return btn

    def add(self):
        value = self.spin.value()
        self.modifyPixels(lambda x, y: x + y, value)

    def subtract(self):
        value = self.spin.value()
        self.modifyPixels(lambda x, y: x - y, value)

    def multiply(self):
        value = self.spin.value()
        self.modifyPixels(lambda x, y: x * y, value)

    def divide(self):
        value = self.spin.value()
        if value == 0:
            print("error")
            return
        self.modifyPixels(lambda x, y: int(x / y), value)

    def changeBrightness(self):
        pass

    def applyMask(self):
        try:
            mask = self.__parseMask()
        except Exception as ex:
            print(str(ex))
            return
        self.__maskImage(mask)

    def setImage(self, image):
        self.originalImage = image
        self.updateImage(image)

    def updateImage(self, image):
        pixmap = QPixmap().fromImage(image)
        self.pixmap_item.setPixmap(pixmap)

    def modifyPixels(self, operation, value):
        image = QImage(self.originalImage)
        for x in range(image.width()):
            for y in range(image.height()):
                rgb = image.pixel(x, y)
                newRgb = qRgb(self.__limitPixel(operation(qRed(rgb), value)),
                              self.__limitPixel(operation(qGreen(rgb), value)),
                              self.__limitPixel(operation(qBlue(rgb), value)))
                image.setPixel(x, y, newRgb)
        self.updateImage(image)

    def saveBtnCommand(self):
        try:
            image = self.pixmap_item.pixmap().toImage()
        except Exception:
            return

        (value, ok) = QInputDialog().getInt(self, "Kompresja", "Stopień kompresji:", 0, 0, 100)
        if not ok:
            return

        fileName = QFileDialog.getSaveFileName(self)
        if not fileName[0]:
            return

        image.save(fileName[0], "jpeg", 100 - value)

    def __maskImage(self, mask: list[list]):
        image = QImage(self.originalImage)
        mask_size = len(mask)
        count = 0
        for row in mask:
            for item in row:
                count = count + item

        if count == 0:
            count = 1
        reach = mask_size - mask_size//2
        for x in range(mask_size//2, image.width()-mask_size//2):
            for y in range(mask_size//2, image.height()-mask_size//2):
                r = 0
                g = 0
                b = 0
                for i in range(mask_size):
                    for j in range(mask_size):
                        oldRgb = self.originalImage.pixel(x + i - reach, y + j - reach)
                        r = r + qRed(oldRgb) * mask[i][j]
                        g = g + qGreen(oldRgb) * mask[i][j]
                        b = b + qBlue(oldRgb) * mask[i][j]
                r = self.__limitPixel(r/count)
                g = self.__limitPixel(g/count)
                b = self.__limitPixel(b/count)
                newRgb = qRgb(r, g, b)
                image.setPixel(x, y, newRgb)
        self.updateImage(image)

    @staticmethod
    def __limitPixel(value):
        return max(min(int(value), 255), 0)

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
