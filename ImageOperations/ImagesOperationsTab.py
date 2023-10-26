import threading

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QFileDialog, QMessageBox, QInputDialog, \
    QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QHBoxLayout

from Files.FilesLoader import FilesLoader
from Files.PpmFile import PpmFile
from Files.SyntaxException import SyntaxException
from ImageOperations.ImageEditor import ImageEditor


class ImagesOperationsTab(QWidget):

    def __init__(self, parent=None):
        super(ImagesOperationsTab, self).__init__(parent)

        self.lay = QHBoxLayout()
        self.setLayout(self.lay)
        self.filesTab = FilesLoader()
        self.lay.addWidget(self.filesTab, stretch=1)

        self.editor = ImageEditor()
        self.filesTab.imageLoaded.connect(self.editor.setImage)
        self.lay.addWidget(self.editor, stretch=2)
