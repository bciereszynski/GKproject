class Polygon:
    def __init__(self, level):
        if type(level) is not int:
            raise Exception("Bad level value: " + str(level))
        self.level = level
        self.points = []
        self.selected = False

    def addPoint(self, point):
        self.points.append(point)

    def isComplete(self):
        return self.level == len(self.points)

    def contains(self, position):
        for p in self.points:
            if p.contains(position):
                return True
        return False

    def move(self, delta):
        for p in self.points:
            p.move(delta)

    def rotate(self, x, y, angle):
        for p in self.points:
            p.rotate(x, y, angle)

    def scale(self, x, y, factorX, factorY):
        for p in self.points:
            p.scale(x, y, factorX, factorY)

    def setSelected(self, isSelected):
        self.selected = isSelected

    def detectPoint(self, position):
        for p in self.points:
            if p.contains(position):
                return p
        return None

    def render(self, painter):
        for p in self.points:
            p.render(painter, self.selected)
        n = len(self.points)
        if n < 2:
            return

        for i in range(n):
            painter.drawLine(self.points[i].x, self.points[i].y,
                             self.points[(i+1) % n].x, self.points[(i+1) % n].y)
