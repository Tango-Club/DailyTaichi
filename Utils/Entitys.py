from shapely.geometry import Point
from shapely.geometry import Polygon


def point_add_point(lhs, rhs):
    return Point(lhs.x + rhs.x, lhs.y + rhs.y)


def point_reverse(lhs):
    return point_multiple(lhs, -1)


def point_multiple(lhs, rhs):
    return Point(lhs.x * rhs, lhs.y * rhs)


def point_max(lhs, rhs):
    return Point(max(lhs.x, rhs.x), max(lhs.y, rhs.y))


def point_min(lhs, rhs):
    return Point(min(lhs.x, rhs.x), min(lhs.y, rhs.y))


class BaseEntity:
    edge: Polygon

    def __init__(self, size, x, y):
        self.size = size
        self.position = Point(x, y)

    def size(self):
        return self.size

    def move(self, rhs):
        self.position = point_add_point(self.position, rhs)


class MoveAbleEntity(BaseEntity):
    speed_max = Point(0, 0)
    position_max = Point(0, 0)

    def __init__(self, size, x, y):
        super().__init__(size, x, y)
        self.speed = Point(0, 0)

    def adapt(self):
        if BaseEntity.edge.crosses(self.position):
            self.speed = point_multiple(point_reverse(self.speed), 0.8)
            print('edge')

        self.speed = point_min(self.speed, type(self).speed_max)
        self.speed = point_max(self.speed, point_reverse(type(self).speed_max))

        if self.position.x >= type(self).position_max.x:
            self.speed = point_add_point(self.speed, Point(-10, 0))
        if self.position.x <= 0:
            self.speed = point_add_point(self.speed, Point(10, 0))
        if self.position.y >= type(self).position_max.y:
            self.speed = point_add_point(self.speed, Point(0, -10))
        if self.position.y <= 0:
            self.speed = point_add_point(self.speed, Point(0, 10))

    def update_speed(self, rhs):
        self.speed = point_add_point(self.speed, rhs)

    def update_position(self):
        self.adapt()
        self.move(self.speed)


class Player(MoveAbleEntity):
    speed_max = Point(10, 10)
    position_max = Point(800, 800)
    pass
