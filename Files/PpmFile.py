from PyQt5.QtGui import QImage, qRgb
from PyQt5.QtWidgets import QFileDialog
from timeit import default_timer as timer

from Files.SyntaxException import SyntaxException


class PpmFile:
    class PpmHeader:
        def __init__(self):
            self.format = None
            self.rows = None
            self.columns = None
            self.colorScale = None

        def isComplete(self):
            return (self.format is not None and self.rows is not None
                    and self.columns is not None and self.colorScale is not None)

    def __init__(self):
        self.header = self.PpmHeader()
        self.currentRgb = []
        self.currentRow = 0
        self.currentCol = 0
        self.image = None

    def load(self, fileName):
        with open(fileName, "rb") as file:
            currentLine = self.__readFileHeader(file)
            lines = file.readlines()

        start = timer()
        self.image = QImage(self.header.columns, self.header.rows, QImage.Format_RGB32)

        # continue where header ends
        words = currentLine.split()
        words = words[words.index(str(self.header.colorScale).encode()) + 1:]
        lines.insert(0, ' '.join(words).encode())

        if self.header.format == "P3":
            self.__readP3FileData(lines)
        elif self.header.format == "P6":
            self.__readP6FileData(lines)
        else:
            raise SyntaxException("Unknown format")

        end = timer()
        print(end - start)

        if self.currentRgb:
            raise SyntaxException("Data not match header - rgb error")
        if self.currentRow != self.header.rows - 1 or self.currentCol != self.header.columns:
            raise SyntaxException("Data not match header - pixels error")
        return self.image

    def __readFileHeader(self, file):
        line = file.readline()
        while line:
            for word in line.split():
                try:
                    if chr(word[0]) == "#":
                        break
                    word = word.decode()
                except UnicodeError:
                    raise SyntaxException("Not ascii symbol in header")

                if self.header.format is None:
                    self.header.format = word
                    if self.header.format != "P3" and self.header.format != "P6":
                        raise SyntaxException("Bad format - " + self.header.format)
                    continue

                try:
                    number = int(word)
                except Exception:
                    raise SyntaxException("Integer expected - " + word)

                if self.header.columns is None:
                    self.header.columns = number
                elif self.header.rows is None:
                    self.header.rows = number
                elif self.header.colorScale is None:
                    self.header.colorScale = number
                    if not 0 < self.header.colorScale < 65536:
                        raise SyntaxException("Invalid color scale")
                    return line
            line = file.readline()
        raise SyntaxException("Header incomplete")

    def addRgb(self, number):
        if self.header.colorScale != 255:
            number = int(number / self.header.colorScale * 255)
        self.currentRgb.append(number)
        if len(self.currentRgb) == 3:
            if self.currentCol >= self.header.columns:
                self.currentCol = 0
                self.currentRow += 1
            value = qRgb(self.currentRgb[0], self.currentRgb[1], self.currentRgb[2])
            self.image.setPixel(self.currentCol, self.currentRow, value)
            self.currentCol += 1
            self.currentRgb = []

    def __readP6FileData(self, lines):
        for line in lines:
            for number in line:
                self.addRgb(number)

    def __readP3FileData(self, lines):
        for line in lines:
            words = line.split()
            for word in words:
                try:
                    if chr(word[0]) == "#":
                        break
                    number = int(word.decode())
                except UnicodeError:
                    raise SyntaxException("Not integer passed")

                self.addRgb(number)
