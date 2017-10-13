
CHUNK_SIZE = 16
TILE_SIZE = 16
SCROLL_SPEED = 75

assets = {}
tiles = {}

class XY:
    def __init__(self, _x=0, _y=0):
        self.x = _x
        self.y = _y
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
