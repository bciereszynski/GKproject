from PyQt5 import QtCore
from PyQt5.QtWidgets import QVBoxLayout, QTabWidget, QWidget, QLabel

from BézierCurve.CurveTab import CurveTab
from Colors.ColorTab import ColorTab
from Files.FilesTab import FilesTab
from Greens.GreenTab import GreenTab
from HistogramAndBinarization.HistogramAndBinarizationTab import HistogramAndBinarizationTab
from ImageOperations.ImagesOperationsTab import ImagesOperationsTab
from Morphology.MorphologyTab import MorphologyTab
from Primitives.PrimitivesTab import PrimitivesTab
from Transformations2D.PolygonTab import PolygonTab


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setGeometry(QtCore.QRect(200, 100, 1200, 600))
        self.setWindowTitle("GK")

        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.primitivesTab = PrimitivesTab()
        self.filesTab = FilesTab()
        self.colorsTab = ColorTab()
        self.imagesOperationsTab = ImagesOperationsTab()
        self.histogramAndBinarizationTab = HistogramAndBinarizationTab()
        self.curveTab = CurveTab()
        self.polygonTab = PolygonTab()
        self.morphologyTab = MorphologyTab()
        self.greenTab = GreenTab()
        self.tabs.resize(300, 200)

        # Add tabs
        self.tabs.addTab(self.primitivesTab, "1. Graphical Primitives")
        self.tabs.addTab(self.filesTab, "2. Files")
        self.tabs.addTab(self.colorsTab, "3. Colors")
        self.tabs.addTab(self.imagesOperationsTab, "4. Images operations")
        self.tabs.addTab(self.histogramAndBinarizationTab, "5. Histogram and binarization")
        self.tabs.addTab(self.curveTab, "6. Beizer curves")
        self.tabs.addTab(self.polygonTab, "7. Polygons")
        self.tabs.addTab(self.morphologyTab, "8. Morphology")
        self.tabs.addTab(self.greenTab, "9. Green")

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        self.authorLabel = QLabel("Author: Bartosz Piotr Ciereszyński")
        self.authorLabel.setAlignment(QtCore.Qt.AlignRight)
        self.layout.addWidget(self.authorLabel)

        self.tabs.setCurrentIndex(5)
