from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage, qBlue, qRed, qRgb, qGreen
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QSpinBox, QLabel, \
    QHBoxLayout, QPushButton, QSlider, QFileDialog, QInputDialog


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

        self.lay.addLayout(self.controlsLay)

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
                newRgb = qRgb(operation(qRed(rgb), value), operation(qGreen(rgb), value), operation(qBlue(rgb), value))
                image.setPixel(x,y,newRgb)
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