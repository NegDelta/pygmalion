from enginemath import XY


def validate(x):
    if x not in {-1, 0, 1}:
        raise ValueError


class Direction:
    def __init__(self, x: int):
        validate(x)
        self.a = x

    def __add__(self, other):
        validate(other)
        if other == 0:
            self.a = other

    def __sub__(self, other):
        validate(other)
        if other == self.a:
            self.a = 0

    def __int__(self):
        return self.a


class XYDirection(XY):
    x: Direction
    y: Direction

    def __init__(self, _x=0, _y=0):
        super().__init__(_x, _y)
        self.x = Direction(int(_x))
        self.y = Direction(int(_y))


DIR_UP = XYDirection(0, -1)
DIR_DOWN = XYDirection(0, 1)
DIR_LEFT = XYDirection(-1, 0)
DIR_RIGHT = XYDirection(1, 0)
