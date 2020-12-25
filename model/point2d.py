import math


class Point2d:

    def __init__(self):
        self.x = 0
        self.y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def set(self, x=0, y=0):
        self.x = x
        self.y = y

    def set(self, point):
        self.x = point.x
        self.y = point.y

    def add(self, point):
        self.x += point.x
        self.y += point.y

    def distance(self, point):
        return math.sqrt(math.pow(self.x - point.x, 2)
                      + math.pow(self.y - point.y, 2))

    def isCollision(self, point, margin=0):
        return self.distance(point) <= margin

    @staticmethod
    def distance_between(p1, p2):
        return math.sqrt(math.pow(p1.x - p2.x, 2) + math.pow(p1.y - p2.y, 2))


    @staticmethod
    def is_collideded(p1, p2, margin):
        return Point2d.distance_between(p1, p2) <= margin
