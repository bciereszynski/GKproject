from PyQt5.QtWidgets import QWidget, QHBoxLayout

from Colors.ColorsWidget import ColorsWidget


class ColorTab(QWidget):

    def __init__(self, parent=None):
        super(ColorTab, self).__init__(parent)

        self.lay = QHBoxLayout()
        self.setLayout(self.lay)

        # self.cubeWidget = CubeWidget()
        # self.lay.addWidget(self.cubeWidget)

        self.colorsWidget = ColorsWidget()
        self.lay.addWidget(self.colorsWidget)
