from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout

from Files.PpmHeader import PpmHeader
from Files.SyntaxException import SyntaxException


class FilesTab(QWidget):
    def __init__(self, parent=None):
        super(FilesTab, self).__init__(parent)

        self.lay = QVBoxLayout()

        self.loadPpmButton = QPushButton("Load PPM")
        self.loadPpmButton.clicked.connect(self.loadPPM)

        self.lay.addWidget(self.loadPpmButton)
        self.setLayout(self.lay)

        self.loadPPM()

    def loadPPM(self):
        with open("C:\\Users\\bcier\\PycharmProjects\\GKproject\\ppm.txt", "r", 2**10) as file:
            header = self.__readFileHeader(file)
            pixels = self.__readP3FileData(file, header)
        print(pixels)

    @staticmethod
    def __readP3FileData(file, header):
        pixels = [[]]
        rgb = []
        currentRow = 0
        line = file.readline()

        while line:
            for word in line.split():
                if word[0] == "#":
                    break
                try:
                    number = int(word)
                except(Exception):
                    raise SyntaxException("Integer expected - " + word)

                rgb.append(number)
                if len(rgb) == 3:
                    if len(pixels[currentRow]) >= header.columns:
                        pixels.append([])
                        currentRow += 1
                    pixels[currentRow].append(rgb)
                    rgb = []
            line = file.readline()

        if rgb != [] or currentRow != header.rows - 1 or len(pixels[currentRow]) != header.columns:
            raise SyntaxException("Data not match header")
        return pixels

    @staticmethod
    def __readFileHeader(file):
        header = PpmHeader()
        line = file.readline()
        while line:
            for word in line.split():
                if word[0] == "#":
                    break
                if header.format is None:
                    header.format = word
                    if header.format != "P3" and format != "P4":
                        raise SyntaxException("Bad format - " + header.format)
                elif header.columns is None:
                    try:
                        header.columns = int(word)
                    except(Exception):
                        raise SyntaxException("Integer expected - " + word)
                elif header.rows is None:
                    try:
                        header.rows = int(word)
                    except(Exception):
                        raise SyntaxException("Integer expected - " + word)
                elif header.colorScale is None:
                    try:
                        header.colorScale = int(word)
                    except(Exception):
                        raise SyntaxException("Integer expected - " + word)
                else:
                    raise SyntaxException("Unexpected token after header - " + word)
            if not header.isComplete():
                line = file.readline()
            else:
                break
        return header
