import threading

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QFileDialog, QMessageBox, QInputDialog

from Files.PpmFile import PpmFile
from Files.SyntaxException import SyntaxException


class FilesTab(QWidget):
    exceptSignal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(FilesTab, self).__init__(parent)

        self.lay = QVBoxLayout()

        self.loadFileButton = QPushButton("Load image file")
        self.loadFileButton.clicked.connect(self.loadBtnCommand)
        self.lay.setAlignment(self.loadFileButton, Qt.AlignTop)
        self.lay.addWidget(self.loadFileButton)

        self.setLayout(self.lay)

        self.label = QLabel()
        self.lay.addWidget(self.label)
        self.lay.setAlignment(self.label, Qt.AlignCenter)

        self.saveFileButton = QPushButton("Save image file")
        self.saveFileButton.clicked.connect(self.saveBtnCommand)
        self.lay.setAlignment(self.saveFileButton, Qt.AlignTop)
        self.lay.addWidget(self.saveFileButton)

        self.exceptSignal.connect(self.__showExceptionMessage)

    def saveBtnCommand(self):
        try:
            image = self.label.pixmap().toImage()
        except Exception:
            self.exceptSignal.emit("No image to save")
            return

        (value, ok) = QInputDialog().getInt(self, "Kompresja", "Stopień kompresji:", 0, 0, 100)
        if not ok:
            return
        
        fileName = QFileDialog.getSaveFileName(self)
        if not fileName[0]:
            return

        image.save(fileName[0], "jpeg", 100 - value)

    def loadBtnCommand(self):
        thread = threading.Thread(target=self.loadFile, args=())
        thread.start()

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
        else:
            self.exceptSignal.emit("File format is not supported - " + fileName[0])
            return

        image = self.__scaleImage(image)
        pixmap = QPixmap().fromImage(image)
        self.label.setPixmap(pixmap)

    def __scaleImage(self, image):
        if image.width() >= image.height():
            if image.width() > 1000:
                image = image.scaledToWidth(self.width() - 20, Qt.SmoothTransformation)
            else:
                image = image.scaledToWidth(self.width() - 20)
        else:
            image = image.scaledToHeight(self.height() - 100)
        return image

    @staticmethod
    def __showExceptionMessage(msg):
        messageBox = QMessageBox()
        messageBox.setText("Error occurred")
        messageBox.setInformativeText(msg)
        messageBox.setIcon(QMessageBox.Warning)
        messageBox.setWindowTitle("Error")
        messageBox.exec()
