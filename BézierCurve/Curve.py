import numpy as np


class Curve:
    def __init__(self, level):
        if type(level) is not int:
            raise Exception("Bad level value: " + str(level))
        self.level = level
        self.points = []
        self.step = 0.05

    def render(self, painter):
        for p in self.points:
            p.render(painter, False)
        if len(self.points) < 2:
            return

        oldX = self.points[0].x
        oldY = self.points[0].y

        for part in np.arange(0, 1, self.step):
            calculatePoints = [(p.x, p.y) for p in self.points]
            while len(calculatePoints) > 1:
                newCalculatePoints = []
                for i in range(len(calculatePoints)-1):
                    newCalculatePoints.append(self.calculateSubCoordinates(calculatePoints[i], calculatePoints[i+1], part))
                calculatePoints = newCalculatePoints
            x = int(calculatePoints[0][0])
            y = int(calculatePoints[0][1])
            painter.drawLine(x, y, oldX, oldY)
            oldX = x
            oldY = y

        painter.drawLine(x, y, self.points[-1].x, self.points[-1].y)


    def setSelected(self, selected):
        if selected:
            return

        for p in self.points:
            p.setSelected(False)

    def addPoint(self, point):
        self.points.append(point)

    def isComplete(self):
        return self.level == len(self.points)

    @staticmethod
    def calculateSubCoordinates(point1, point2, t):
        dx = point2[0] - point1[0]
        dy = point2[1] - point1[1]
        return point1[0] + dx * t, point1[1] + dy * t
