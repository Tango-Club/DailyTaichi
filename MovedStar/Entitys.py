from MovedStar.Utils2D import Vector2D, Point2D


class BaseEntity:
    def __init__(self, size, x, y):
        self.size = size
        self.position = Point2D(x, y)

    def add(self, rhs):
        self.position.add(rhs)

    def sub(self, rhs):
        self.position.sub(rhs)

    def size(self):
        return self.size

    def move(self, rhs: Vector2D):
        self.position.add(rhs)

    def x(self):
        return self.position.x

    def y(self):
        return self.position.y


class MoveAbleEntity(BaseEntity):
    def __init__(self, size, x, y):
        self.position = BaseEntity(size, x, y)
        self.speed = Vector2D(0, 0)

    def update_speed(self, rhs: Vector2D):
        self.speed.add(rhs)

    def update_position(self):
        self.position.add(self.speed)


class Player(MoveAbleEntity):
    pass
