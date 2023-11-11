from PyQt5.QtWidgets import QWidget, QHBoxLayout

from Files.FilesLoader import FilesLoader
from ImageOperations.PixelEditor import PixelEditor


class ImagesOperationsTab(QWidget):

    def __init__(self, parent=None):
        super(ImagesOperationsTab, self).__init__(parent)

        self.lay = QHBoxLayout()
        self.setLayout(self.lay)
        self.filesTab = FilesLoader()
        self.lay.addWidget(self.filesTab, stretch=1)

        self.editor = PixelEditor()
        self.filesTab.imageLoaded.connect(self.editor.setImage)
        self.lay.addWidget(self.editor, stretch=2)
