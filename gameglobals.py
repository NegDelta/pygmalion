import numbers

TILE_SIZE = 256
CHUNK_SIZE = 16
DISPLAY_FACTOR = 16
TILE_SCRSIZE = TILE_SIZE / DISPLAY_FACTOR
CHUNK_PIXSIZE = CHUNK_SIZE * TILE_SIZE
CHUNK_SCRSIZE = CHUNK_SIZE * TILE_SCRSIZE
SCROLL_SPEED = 75*16

assets = {}
tiles = {}

class XY:
    def __init__(self, _x=0, _y=0):
        try: # try to initialize from iterable
            if len(_x) >= 2:
                self.x = _x[0]
                self.y = _x[1]
                return
        except TypeError:
            if (not isinstance(_x, numbers.Number)) or \
               (not isinstance(_y, numbers.Number)):
                raise TypeError('XY: Not a number ({}, {})'.format(_x, _y))
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
        return (self.x, self.y)
    
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
        self.x = int(self.x)
        self.y = int(self.y)
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

    def xylen(self):
        return (self.x**2 + self.y**2) ** 0.5

class Camera:
    def __init__(self):
        self.rect = _rect
        self.tilemap = _map
        
    def record(self):
        pass