import numbers


# Sign fn
def sgn(x) -> int:
    if x > 0:
        return 1
    elif x < 0:
        return -1
    elif x == 0:
        return 0
    raise TypeError


# Floor. Works down, not towards 0
def floor(x) -> int:
    return x//1


# Interpolate between x0 (for k=0) & x1 (for k=1)
def ipol(x0, x1, k):
    return x0 + (x1-x0) * k


# Get factor from interpolated value
def rev_ipol(x0, x1, x):
    try:
        return (x - x0)/(x1 - x0)
    except ZeroDivisionError:
        return 0


# React to movement key being pressed
def diradd(p1, p2):
    if p1[0] == 0:
        p1[0] = p2[0]
    if p1[1] == 0:
        p1[1] = p2[1]
    return p1


# React to movement key being released
def dirsub(p1, p2):
    if p1[0]*p2[0] > 0:  # signs match and non-zero
        p1[0] = 0
    if p1[1]*p2[1] > 0:
        p1[1] = 0
    return p1


# Return coordinate offset from block that point is in
# and border about to be hit with given velocity
def getborder(dirv) -> int:
    return int(dirv > 0)


class XY:
    x: numbers.Real
    y: numbers.Real

    def __init__(self, _x: numbers.Real, _y: numbers.Real):
        self.x = _x
        self.y = _y

    def __repr__(self):
        return '<XY({}, {})>'.format(self.x, self.y)

    # index syntax (x[0], x[1]) for compatibility w/ iterables
    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            raise IndexError

    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        else:
            raise IndexError

    def totuple(self):
        return self.x, self.y

    # arithmetics
    def __add__(self, other):
        return XY(
            self.x + other.x,
            self.y + other.y
        )

    def __sub__(self, other):
        return XY(
            self.x - other.x,
            self.y - other.y
        )

    def __mul__(self, other):
        return XY(
            self.x * other,
            self.y * other
        )

    def __truediv__(self, other):
        return XY(
            self.x / other,
            self.y / other
        )

    def __floordiv__(self, other):
        return XY(
            self.x // other,
            self.y // other
        )

    def intize(self):
        self.x = int(floor(self.x))
        self.y = int(floor(self.y))
        return self

    def __mod__(self, other):
        if type(other) == XY:
            return XY(
                self.x % other.x,
                self.y % other.y
            )
        else:
            return XY(
                self.x % other,
                self.y % other
            )

    def flipx(self):
        self.x *= -1
        return self

    def flipy(self):
        self.y *= -1
        return self

    def floor(self):
        self.x = int(floor(self.x))
        self.y = int(floor(self.y))
        return self

    def xylen(self):
        return (self.x**2 + self.y**2) ** 0.5


# Return vector of same direction but of given length
def unitize(v: XY, length=1) -> XY:
    veclen = (v.x**2 + v.y**2) ** 0.5
    if veclen == 0:
        return v
    else:
        return v * (length / veclen)
