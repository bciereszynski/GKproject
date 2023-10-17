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
        start = timer()
        with open(fileName, "rb") as file:
            currentLine = self.__readFileHeader(file)
            data = file.read()

        self.image = QImage(self.header.columns, self.header.rows, QImage.Format_RGB32)

        if self.header.format == "P3":
            # continue where header ends
            words = currentLine.split()
            words = words[words.index(str(self.header.colorScale).encode()) + 1:]  # problem width or height = scale
            words = [byte.decode() for byte in words]
            data = ' '.join(words).encode() + "\n".encode() + data
            self.__readP3FileData(data)
        elif self.header.format == "P6":
            self.__readP6FileData(data)
        else:
            raise SyntaxException("Unknown format")

        end = timer()
        print(end - start)

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

    def __readP6FileData(self, data):
        try:
            self.image = QImage(data, self.header.columns, self.header.rows, self.header.columns*3, QImage.Format_RGB888)
        except:
            raise SyntaxException("File data corrupted")

    def __readP3FileData(self, data):

        begin = data.find("#".encode())
        while begin != -1:
            end = data.find("\n".encode(), begin)
            data = data[:begin-1] + data[end:]
            begin = data.find("#".encode(), end)

        if self.header.colorScale != 255:
            data = [int(int(byte.decode())/self.header.colorScale * 255) for byte in data.split()]
        else:
            data = [int(byte.decode()) for byte in data.split()]

        data = bytes(data)

        try:
            self.image = QImage(data, self.header.columns, self.header.rows, self.header.columns*3, QImage.Format_RGB888)
        except:
            raise SyntaxException("File data corrupted")
