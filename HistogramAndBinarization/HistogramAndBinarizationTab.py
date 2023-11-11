from PyQt5.QtWidgets import QWidget, QHBoxLayout

from Files.FilesLoader import FilesLoader
from HistogramAndBinarization.HistogramEditor import HistogramEditor


class HistogramAndBinarizationTab(QWidget):

    def __init__(self, parent=None):
        super(HistogramAndBinarizationTab, self).__init__(parent)

        self.lay = QHBoxLayout()
        self.filesTab = FilesLoader()
        self.lay.addWidget(self.filesTab, stretch=1)

        self.editor = HistogramEditor()
        self.filesTab.imageLoaded.connect(self.editor.setImage)
        self.lay.addWidget(self.editor, stretch=2)

        self.setLayout(self.lay)
