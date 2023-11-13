import numpy as np


class Curve:
    def __init__(self, level):
        if type(level) is not int:
            raise Exception("Bad level value: " + str(level))
        self.level = level
        self.points = []
        self.curvePoints = None
        self.step = 0.05

        self.__selectedPoint = None

    def addPoint(self, point):
        self.points.append(point)
        self.curvePoints = None

    def editPoint(self, point, index):
        self.points[index] = point
        self.curvePoints = None

    def deletePoint(self, point):
        self.points.remove(point)
        self.curvePoints = None

    def render(self, painter):
        for p in self.points:
            if self.__selectedPoint is not None and p == self.__selectedPoint:
                p.render(painter, True)
            p.render(painter, False)
        if len(self.points) < 2:
            return

        if self.curvePoints is None:
            self.__calculateCurve()

        for i in range(len(self.curvePoints)-1):
            painter.drawLine(self.curvePoints[i][0], self.curvePoints[i][1],
                             self.curvePoints[i+1][0], self.curvePoints[i+1][1])

    def __calculateCurve(self):
        def calculateSubPoint(point1, point2, t):
            dx = point2[0] - point1[0]
            dy = point2[1] - point1[1]
            return point1[0] + dx * t, point1[1] + dy * t

        self.curvePoints = [(self.points[0].x, self.points[0].y)]
        for part in np.arange(0, 1, self.step):
            points = [(p.x, p.y) for p in self.points]
            while len(points) > 1:
                newPoints = []
                for i in range(len(points) - 1):
                    newPoints.append(
                        calculateSubPoint(points[i], points[i + 1], part))
                points = newPoints
            self.curvePoints.append((int(points[0][0]), int(points[0][1])))
        self.curvePoints.append((self.points[-1].x, self.points[-1].y))

    def setSelected(self, selected, point=None):
        if point is not None:
            if selected:
                self.__selectedPoint = point
            else:
                self.__selectedPoint = None

    def isComplete(self):
        return self.level == len(self.points)

    def contains(self, position):
        for p in self.points:
            if p.contains(position):
                return True, p

        return False, None
