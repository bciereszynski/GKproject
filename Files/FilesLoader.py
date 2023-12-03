import threading

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QFileDialog, QMessageBox, QInputDialog, \
    QGraphicsView, QGraphicsScene, QGraphicsPixmapItem

from Files.PpmFile import PpmFile
from Files.SyntaxException import SyntaxException


class FilesLoader(QWidget):
    exceptSignal = pyqtSignal(str)
    imageLoaded = pyqtSignal(QImage)

    def __init__(self, parent=None):
        super(FilesLoader, self).__init__(parent)

        self.lay = QVBoxLayout()

        self.loadFileButton = QPushButton("Load image file")
        self.loadFileButton.clicked.connect(self.loadFile)
        self.lay.setAlignment(self.loadFileButton, Qt.AlignTop)
        self.lay.addWidget(self.loadFileButton)

        self.setLayout(self.lay)

        self.view = self.view = QGraphicsView(self)
        self.lay.addWidget(self.view)

        self.scene = QGraphicsScene(self)
        self.view.setScene(self.scene)

        self.pixmap_item = QGraphicsPixmapItem()
        self.scene.addItem(self.pixmap_item)

        self.exceptSignal.connect(self.__showExceptionMessage)

    def loadFile(self):
        fileName = QFileDialog.getOpenFileName(self)
        if not fileName[0]:
            return

        if fileName[0].find(".ppm") != -1:
            file = PpmFile()
            try:
                image = file.load(fileName[0])
            except SyntaxException as ex:
                self.exceptSignal.emit(ex.message)
                return
        elif fileName[0].find(".jpg") != -1 or fileName[0].find(".jpeg") != -1:
            image = QImage()
            try:
                image.load(fileName[0], "jpeg")
            except:
                self.exceptSignal.emit("Error occurred during file load - " + fileName[0])
        elif fileName[0].find(".png") != -1:
            image = QImage()
            try:
                image.load(fileName[0], "png")
            except:
                self.exceptSignal.emit("Error occurred during file load - " + fileName[0])
        else:
            self.exceptSignal.emit("File format is not supported - " + fileName[0])
            return

        image = self.__scaleImage(image)
        pixmap = QPixmap().fromImage(image)
        self.imageLoaded.emit(image)

        self.pixmap_item.setPixmap(pixmap)

    def __scaleImage(self, image):
        if image.width() >= image.height():
            if image.width() > 100 or image.height() > 100:
                image = image.scaledToWidth(self.view.width(), Qt.SmoothTransformation)
            else:
                image = image.scaledToWidth(self.view.width())
        else:
            image = image.scaledToHeight(self.view.height())
        return image

    @staticmethod
    def __showExceptionMessage(msg):
        messageBox = QMessageBox()
        messageBox.setText("Error occurred")
        messageBox.setInformativeText(msg)
        messageBox.setIcon(QMessageBox.Warning)
        messageBox.setWindowTitle("Error")
        messageBox.exec()
