from Primitives.Menu import Menu
from PyQt5.QtWidgets import QPushButton, QFileDialog


class DataMenu(Menu):

    def __init__(self, paint, parent=None):
        super().__init__(parent)

        self.paint = paint

        self.saveButton = self.createButton("Save", self.save)
        self.loadButton = self.createButton("Load", self.load)

    def save(self):
        fileName = QFileDialog.getSaveFileName(self)
        if fileName[0]:
            self.paint.saveData(fileName[0])

    def load(self):
        fileName = QFileDialog.getOpenFileName(self)
        if fileName[0]:
            self.paint.loadData(fileName[0])
