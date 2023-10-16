import threading
from timeit import default_timer as timer

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, qRgb, QPixmap
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QFileDialog

from Files.PpmHeader import PpmHeader
from Files.SyntaxException import SyntaxException


class FilesTab(QWidget):
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

    def loadBtnCommand(self):
        thread = threading.Thread(target=self.loadPPM, args=())
        thread.start()

    def loadPPM(self):

        fileName = QFileDialog.getOpenFileName(self)
        start = timer()
        if not fileName[0]:
            return

        with open(fileName[0], "r") as file:
            lines = file.readlines()

        header, currentLine = self.__readFileHeader(lines)

        image = QImage(header.columns, header.rows, QImage.Format_RGB32)
        self.__readP3FileData(lines, header, image)

        end = timer()
        print(end - start)
        image = image.scaledToWidth(1200)
        image = image.scaledToHeight(600)
        pixmap = QPixmap().fromImage(image)
        self.label.setPixmap(pixmap)

    @staticmethod
    def __readP3FileData(lines, header, image):
        rgb = []
        currentRow = 0
        currentCol = 0

        # continue where header ends
        line = lines[0]
        words = line.split()
        words = words[words.index(str(header.colorScale))+1:]

        for line in lines:
            if words is None:
                words = line.split()
            for word in words:
                if word[0] == "#":
                    break
                try:
                    number = int(word)
                except Exception:
                    raise SyntaxException("Integer expected - " + word)

                rgb.append(number)
                if len(rgb) == 3:
                    if currentCol >= header.columns:
                        currentCol = 0
                        currentRow += 1
                    value = qRgb(rgb[0], rgb[1], rgb[2])
                    image.setPixel(currentCol, currentRow, value)
                    currentCol += 1
                    rgb = []
            words = None

        if rgb:
            raise SyntaxException("Data not match header - rgb error")
        if currentRow != header.rows - 1 or currentCol != header.columns:
            raise SyntaxException("Data not match header - pixels error")

    @staticmethod
    def __readFileHeader(lines):
        header = PpmHeader()
        while lines:
            line = lines[0]
            for word in line.split():
                if word[0] == "#":
                    break
                if header.format is None:
                    header.format = word
                    if header.format != "P3" and format != "P6":
                        raise SyntaxException("Bad format - " + header.format)
                elif header.columns is None:
                    try:
                        header.columns = int(word)
                    except Exception:
                        raise SyntaxException("Integer expected - " + word)
                elif header.rows is None:
                    try:
                        header.rows = int(word)
                    except Exception:
                        raise SyntaxException("Integer expected - " + word)
                elif header.colorScale is None:
                    try:
                        header.colorScale = int(word)
                    except Exception:
                        raise SyntaxException("Integer expected - " + word)
                    return header, line
            lines.remove(line)
        raise SyntaxException("Header incomplete")
