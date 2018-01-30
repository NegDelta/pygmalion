import random
from gameglobals import *

# TODO: relegate generator to arbitrary function
# TODO: add support for partial initialization
class Chunk:
    default_id = 0
    
    def __init__ (self, _cx, _cy):
        self.cx = _cx
        self.cy = _cy
        self.initgrund()
    
    # Generators. TODO: isolate of move to main
    def initbaka(self):
        self.contents = []
        for i in range(0, CHUNK_SIZE):
            self.contents += [[self.default_id] * CHUNK_SIZE]
        self.contents[1][1] = 1
    def initgrund(self):
        if self.cy < 0:
            self.contents = [[0] * CHUNK_SIZE] * CHUNK_SIZE
        elif self.cy > 0:
            self.contents = [[1] * CHUNK_SIZE] * CHUNK_SIZE
        else:
            self.contents = []
            for i in range(0, CHUNK_SIZE):
                self.contents += [[]]
                for j in range(0, CHUNK_SIZE):
                    if j / CHUNK_SIZE > random.random():
                        self.contents[i] += [1]
                    else:
                        self.contents[i] += [0]
    
    # Get/Set tiletype from within chunk
    def get(self, _tx, _ty):
        return self.contents[_tx][_ty]
    def set_to(self, _tx, _ty, val):
        self.contents[_tx][_ty] = val

# This class stores info on TYPE, not any particular tile
class Tile:
    def __init__(self, _name, _coll):
        self.name = _name           # Name, doubling as sprite index
        self.sprite = assets[_name]
        self.coll = _coll           # Physical properties

class Tilemap:
    def __init__(self):
        self.chunks = {}
    
    # Get/Set tiletype of a single tile from within a tilemap
    def get(self, _tx, _ty):
        cx = _tx // CHUNK_SIZE
        cy = _ty // CHUNK_SIZE
        tx = _tx % CHUNK_SIZE
        ty = _ty % CHUNK_SIZE
        return self.getchunk(cx,cy).get(tx,ty)
    def set_to(self, _tx, _ty, val):
        cx = _tx // CHUNK_SIZE
        cy = _ty // CHUNK_SIZE
        tx = _tx % CHUNK_SIZE
        ty = _ty % CHUNK_SIZE
        self.getchunk(cx,cy).set_to(tx,ty,val)
    
    # Get a single chunk from within a tilemap
    def getchunk(self, _cx, _cy):
        if not (_cx, _cy) in self.chunks.keys():
            self.chunks[_cx,_cy] = Chunk(_cx,_cy)
        return self.chunks[_cx,_cy]
        
    # Render a given area of tiles onto a surface
    def render(self, area, sur):
        #area is a Rect, sur a Suface
        for ix in range(area.x, area.x + area.width + 1, TILE_SIZE):
            for iy in range(area.y, area.y + area.height + 1, TILE_SIZE):
                sur.blit(
                    tiles[self.get(ix // TILE_SIZE, iy // TILE_SIZE)].sprite,
                    (
                        ix - area.x - (area.x % TILE_SIZE),
                        iy - area.y - (area.y % TILE_SIZE)
                    )
                )

# Convert point XY with epsilon data to tile XY index
def gettilefrompt(pt, eps=[0,0]):
    return [
        int(pt[0] // TILE_SIZE - (eps[0] < 0 and pt[0] % TILE_SIZE == 0)),
        int(pt[1] // TILE_SIZE - (eps[1] < 0 and pt[1] % TILE_SIZE == 0))
    ]
