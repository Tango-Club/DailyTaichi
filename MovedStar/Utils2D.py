import math


class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, x, y):
        self.x += x
        self.y += y

    def sub(self, x, y):
        self.x -= x
        self.y -= y

    def add(self, rhs):
        self.x += rhs.x
        self.y += rhs.y

    def sub(self, rhs):
        self.x -= rhs.x
        self.y -= rhs.y

    def magnitude2(self):
        return self.x * self.x + self.y * self.y

    def magnitude(self):
        return math.sqrt(self.magnitude2())


class Point2D(Vector2D):
    def distance2(self, rhs):
        return (rhs.x - self.x)**2 + (rhs.y - self.y)**2

    def distance(self, rhs):
        return math.sqrt(self.distance2(rhs))
