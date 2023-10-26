from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QInputDialog, QFileDialog

from Files.FilesLoader import FilesLoader


class FilesTab(QWidget):

    def __init__(self, parent=None):
        super(FilesTab, self).__init__(parent)
        self.lay = QVBoxLayout()
        self.loader = FilesLoader()
        self.setLayout(self.lay)
        self.lay.addWidget(self.loader)

        self.saveFileButton = QPushButton("Save image file")
        self.saveFileButton.clicked.connect(self.saveBtnCommand)
        self.lay.setAlignment(self.saveFileButton, Qt.AlignTop)
        self.lay.addWidget(self.saveFileButton)

    def saveBtnCommand(self):
        try:
            image = self.loader.pixmap_item.pixmap().toImage()
        except Exception:
            self.loader.exceptSignal.emit("No image to save")
            return

        (value, ok) = QInputDialog().getInt(self, "Kompresja", "Stopień kompresji:", 0, 0, 100)
        if not ok:
            return

        fileName = QFileDialog.getSaveFileName(self)
        if not fileName[0]:
            return

        image.save(fileName[0], "jpeg", 100 - value)
