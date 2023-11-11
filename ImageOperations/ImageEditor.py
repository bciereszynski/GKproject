from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage, qGreen, qRed, qBlue, qRgb
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QVBoxLayout, QInputDialog, QFileDialog, QGraphicsView, \
    QGraphicsScene, QGraphicsPixmapItem


class ImageEditor(QWidget):
    def __init__(self, parent=None):
        super(ImageEditor, self).__init__(parent)
        self.lay = QHBoxLayout()
        self.setLayout(self.lay)

        self.currentImage = None
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

        self.resetBtn = QPushButton("Reset")
        self.resetBtn.clicked.connect(self.reset)

        self.imageLayout.addWidget(self.saveFileButton)
        self.imageLayout.addWidget(self.view)
        self.imageLayout.addWidget(self.resetBtn)

        self.lay.addLayout(self.imageLayout, stretch=3)

        self.controlsLay = QVBoxLayout()
        self.controlsLay.setAlignment(Qt.AlignTop)

        self.lay.addLayout(self.controlsLay, stretch=1)

    def createControlButton(self, name, action):
        btn = QPushButton(name)
        btn.clicked.connect(action)
        self.controlsLay.addWidget(btn)
        return btn

    def setImage(self, image):
        self.originalImage = image
        self.updateImage(image)

    def updateImage(self, image):
        pixmap = QPixmap().fromImage(image)
        self.pixmap_item.setPixmap(pixmap)
        self.currentImage = image

    def saveBtnCommand(self):
        try:
            image = self.pixmap_item.pixmap().toImage()
        except Exception:
            return

        (value, ok) = QInputDialog().getInt(self, "Kompresja",
                                            "Stopień kompresji:", 0, 0, 100)
        if not ok:
            return

        fileName = QFileDialog.getSaveFileName(self)
        if not fileName[0]:
            return

        image.save(fileName[0], "jpeg", 100 - value)

    def reset(self):
        self.updateImage(self.originalImage)

    def toGrayscaleLinear(self):
        image = QImage(self.currentImage)
        for x in range(image.width()):
            for y in range(image.height()):
                rgb = image.pixel(x, y)
                r = qRed(rgb)
                g = qGreen(rgb)
                b = qBlue(rgb)
                gray = int(0.2989 * r + 0.5870 * g + 0.1140 * b)
                rgb = qRgb(gray, gray, gray)
                image.setPixel(x, y, rgb)
        self.updateImage(image)

    @staticmethod
    def limitPixel(value):
        return max(min(int(value), 255), 0)
