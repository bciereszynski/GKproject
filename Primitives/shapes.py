from PyQt5.QtCore import QPoint
import math
from abc import ABC, abstractmethod


class Shape(ABC):
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
        self._resizePoint = point2
        self.isSelected = False

    def render(self, painter):
        self.point1.render(painter, self.isSelected)
        self.point2.render(painter, self.isSelected)

    def setSelected(self, isSelected):
        self.isSelected = isSelected

    def resize(self, delta):
        if self._resizePoint is not None:
            self._resizePoint.resize(delta)

    def move(self, delta):
        self.point1.move(delta)
        self.point2.move(delta)

    @abstractmethod
    def contains(self, position):
        pass

    def checkResize(self, position):
        if self.point1.contains(position):
            self._resizePoint = self.point1
            return True
        if self.point2.contains(position):
            self._resizePoint = self.point2
            return True
        return False

    def checkMove(self, position):
        if self.contains(position) and not self.point2.contains(position):
            return True
        return False


class Line(Shape):
    def __init__(self, point1, point2):
        super().__init__(point1, point2)
        self._tolerance = 1

    def render(self, painter):
        super().render(painter)
        painter.drawLine(self.point1.x, self.point1.y, self.point2.x, self.point2.y)

    def contains(self, position):
        distP1P2 = math.sqrt(math.pow(self.point1.x-self.point2.x, 2) + math.pow(self.point1.y - self.point2.y, 2))
        distP1Poz = math.sqrt(math.pow(self.point1.x - position.x(), 2) + math.pow(self.point1.y - position.y(), 2))
        distP2Poz = math.sqrt(math.pow(self.point2.x - position.x(), 2) + math.pow(self.point2.y - position.y(), 2))

        if abs(distP1P2 - distP1Poz - distP2Poz) < self._tolerance:
            return True

        return False


class Circle(Shape):
    def __init__(self, point1, point2):
        super().__init__(point1, point2)
        self.r = None

    def render(self, painter):
        super().render(painter)
        self.r = math.sqrt(math.pow(self.point1.x - self.point2.x, 2) + math.pow(self.point1.y - self.point2.y, 2))
        painter.drawEllipse(QPoint(self.point1.x, self.point1.y), int(self.r), int(self.r))

    def contains(self, position):
        if self.r is None:
            self.r = math.sqrt(math.pow(self.point1.x - self.point2.x, 2) + math.pow(self.point1.y - self.point2.y, 2))
        distance = math.sqrt(math.pow(self.point1.x - position.x(), 2) + math.pow(self.point1.y - position.y(), 2))
        if distance < self.r:
            return True
        return False


class Rectangle(Shape):
    def __init__(self, point1, point2):
        super().__init__(point1, point2)

    def render(self, painter):
        super().render(painter)
        painter.drawRect(self.point1.x, self.point1.y, self.point2.x-self.point1.x, self.point2.y-self.point1.y)

    def contains(self, position):
        max_x = max(self.point1.x, self.point2.x)
        min_x = min(self.point1.x, self.point2.x)
        max_y = max(self.point1.y, self.point2.y)
        min_y = min(self.point1.y, self.point2.y)
        if min_x < position.x() < max_x and min_y < position.y() < max_y:
            return True
        return False
