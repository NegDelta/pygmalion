import random
from gameglobals import *

# TODO: relegate generator to arbitrary function
# TODO: add support for partial initialization
class Chunk:
    default_id = 0
    
    def __init__ (self, _index):
        self.index = _index
        self.initgrund()
    
    # Generators. TODO: isolate of move to main
    def initbaka(self):
        print('Generating chunk ', self.index) #
        self.contents = []
        for i in range(0, CHUNK_SIZE):
            self.contents += [[self.default_id] * CHUNK_SIZE]
        self.contents[1][1] = 1
    def initgrund(self):
        if self.index.y < 0:
            self.contents = [[0] * CHUNK_SIZE] * CHUNK_SIZE
        elif self.index.y > 0:
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
    def get(self, _tindex):
        return self.contents[_tindex.x][_tindex.y]
    def set_to(self, _tindex, val):
        self.contents[_tindex.x][_tindex.y] = val

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
    def get(self, _tindex):
        if type(_tindex) != XY:
            _tindex = XY(_tindex)
        cindex = _tindex // CHUNK_SIZE
        tindex = _tindex % CHUNK_SIZE
        return self.getchunk(cindex).get(tindex)
    def set_to(self, _tindex, val):
        if type(_tindex) != XY:
            _tindex = XY(_tindex)
        cindex = _tindex // CHUNK_SIZE
        tindex = _tindex % CHUNK_SIZE
        self.getchunk(cindex).set_to(tindex,val)
    
    # Get a single chunk from within a tilemap
    def getchunk(self, _cindex):
        if not (_cindex.totuple()) in self.chunks.keys():
            self.chunks[_cindex.totuple()] = Chunk(_cindex)
        return self.chunks[_cindex.totuple()]
        
    # Render a given area of tiles onto a surface
    def render(self, area, sur):
        #area is a Rect, sur a Suface
        #ix, iy iterate over places where tiles need to be rendered (bottom-right)
        for ix in range(area.x, area.x + area.width + 1, TILE_SIZE):
            for iy in range(area.y, area.y + area.height + 1, TILE_SIZE):
                sur.blit(
                    tiles[self.get(XY(ix, iy) // TILE_SIZE)].sprite, # sprite in point i
                    (
                        ix - area.x - (area.x % TILE_SIZE),
                        iy - area.y - (area.y % TILE_SIZE)
                    )
                )

# Convert point XY with epsilon data to tile XY index
def gettilefrompt(pt, eps=XY(0,0)):
    return [
        int(pt[0] // TILE_SIZE - (eps[0] < 0 and pt[0] % TILE_SIZE == 0)),
        int(pt[1] // TILE_SIZE - (eps[1] < 0 and pt[1] % TILE_SIZE == 0))
    ]
