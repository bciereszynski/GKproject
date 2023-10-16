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

    def loadPPM(self):
        with open("C:\\Users\\bcier\\PycharmProjects\\GKproject\\ppm-big.ppm", "r") as file:
            lines = file.readlines()
        header, currentLine = self.__readFileHeader(lines)
        lineIndex = lines.index(currentLine)
        lines = lines[lineIndex:]
        pixels = self.__readP3FileData(lines, header)
        print(pixels)

    @staticmethod
    def __readP3FileData(lines, header):
        pixels = [[]]
        rgb = []
        currentRow = 0

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
                except(Exception):
                    raise SyntaxException("Integer expected - " + word)

                rgb.append(number)
                if len(rgb) == 3:
                    if len(pixels[currentRow]) >= header.columns:
                        pixels.append([])
                        currentRow += 1
                    pixels[currentRow].append(rgb)
                    rgb = []
                words = None

        if rgb != [] or currentRow != header.rows - 1 or len(pixels[currentRow]) != header.columns:
            raise SyntaxException("Data not match header")
        return pixels

    @staticmethod
    def __readFileHeader(lines):
        header = PpmHeader()
        for line in lines:
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
                    return header, line
        raise SyntaxException("Header incomplete")
