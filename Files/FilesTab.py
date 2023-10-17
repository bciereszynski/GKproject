import threading

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QFileDialog, QMessageBox

from Files.PpmFile import PpmFile
from Files.SyntaxException import SyntaxException


class FilesTab(QWidget):
    exceptSignal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(FilesTab, self).__init__(parent)

        self.lay = QVBoxLayout()

        self.loadPpmButton = QPushButton("Load PPM")
        self.loadPpmButton.clicked.connect(self.loadBtnCommand)
        self.lay.setAlignment(self.loadPpmButton, Qt.AlignTop)

        self.lay.addWidget(self.loadPpmButton)
        self.setLayout(self.lay)

        self.label = QLabel()
        self.lay.addWidget(self.label)
        self.lay.setAlignment(self.label, Qt.AlignCenter)

        self.exceptSignal.connect(self.__showExceptionMessage)

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
        else:
            self.exceptSignal.emit("File format is not supported - " + fileName[0])
            return

        image = image.scaledToWidth(1200)
        image = image.scaledToHeight(600)
        pixmap = QPixmap().fromImage(image)
        self.label.setPixmap(pixmap)

    @staticmethod
    def __showExceptionMessage(msg):
        messageBox = QMessageBox()
        messageBox.setText("Error occurred")
        messageBox.setInformativeText(msg)
        messageBox.setIcon(QMessageBox.Warning)
        messageBox.setWindowTitle("Error")
        messageBox.exec()
