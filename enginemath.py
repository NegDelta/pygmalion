import numbers


def sgn(x) -> int:
    """Return -1, 0 or 1, depending on input sign."""
    if x > 0:
        return 1
    elif x < 0:
        return -1
    elif x == 0:
        return 0
    raise TypeError


def floor(x) -> int:
    """Round down (not towards 0)."""
    return x//1


def ipol(x0, x1, k):
    """Interpolate between x0 (for k=0) and x1 (for k=1)."""
    return x0 + (x1-x0) * k


def rev_ipol(x0, x1, x, default=0):
    """Get factor from interpolated value.
    :param x0: Value corresponding to k=0
    :param x1: Value corresponding to k=1
    :param x: Interpolated value to calculate factor for
    :param default: Default value for x0=x1
    :return: The factor k
    """
    try:
        return (x - x0)/(x1 - x0)
    except ZeroDivisionError:
        return 0


def diradd(p1, p2):
    """React to pressing a movement key."""
    if p1[0] == 0:
        p1[0] = p2[0]
    if p1[1] == 0:
        p1[1] = p2[1]
    return p1


def dirsub(p1, p2):
    """React to releasing a movement key."""
    if p1[0]*p2[0] > 0:  # signs match and non-zero
        p1[0] = 0
    if p1[1]*p2[1] > 0:
        p1[1] = 0
    return p1


def getborder(dirv) -> int:
    """
    Get coordinate offset from block that point is in
    and border about to be hit with given velocity
    :param dirv: Velocity direction
    :return: Coordinate offset
    """
    return int(dirv > 0)


class XY:
    x: numbers.Real
    y: numbers.Real

    def __init__(self, *args):
        if len(args) == 1:  # XY
            self.x, self.y = args[0]
        elif len(args) == 2:  # Number, Number
            self.x, self.y = args
        elif len(args) == 0:
            self.x, self.y = 0, 0
        else:
            raise SyntaxError("Wrong number of arguments")

    def __repr__(self):
        return '<XY({}, {})>'.format(self.x, self.y)

    def __getitem__(self, key):
        """Return fields from index syntax (x[0], x[1]) for compatibility w/ iterables."""
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

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

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

    def unitize(self, length=1):
        """Normalize to unit or given length."""
        veclen = (self.x**2 + self.y**2) ** 0.5
        if veclen == 0:
            return self
        else:
            return self * (length / veclen)
