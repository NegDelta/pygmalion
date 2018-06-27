import pygame
import random
from gameglobals import *

# TODO: add support for partial initialization
class Chunk:
    default_id = 0
    
    def __init__ (self, _index):
        self.index = _index
        self.initmap()
        self.image = pygame.Surface((int(CHUNK_SCRSIZE), int(CHUNK_SCRSIZE)))
        
        for ix in range(0, CHUNK_SIZE):
            for iy in range(0, CHUNK_SIZE):
                try:
                    self.image.blit(
                        tiles[self.get(XY(ix,iy))].sprite, # sprite in tile i
                        (
                            ix * TILE_SIZE / DISPLAY_FACTOR,
                            iy * TILE_SIZE / DISPLAY_FACTOR
                        )
                    )
                except TypeError:
                    print(self.contents[ix])
                    raise
                    
    def initmap(self):
        self.initgrund()
    
    # Generators. TODO: isolate or move to main
    def initbaka(self):
        print('Generating chunk ', self.index) #
        self.contents = []
        for i in range(0, CHUNK_SIZE):
            self.contents.append([[self.default_id] * CHUNK_SIZE])
        self.contents[1][1] = 1
    def initgrund(self):
        if self.index.y < 0:
            self.contents = [[0] * CHUNK_SIZE] * CHUNK_SIZE
        elif self.index.y > 0:
            self.contents = [[1] * CHUNK_SIZE] * CHUNK_SIZE
        else:
            self.contents = []
            for i in range(0, CHUNK_SIZE):
                self.contents.append([])
                for j in range(0, CHUNK_SIZE):
                    if j / CHUNK_SIZE > random.random():
                        self.contents[i].append(1)
                    else:
                        self.contents[i].append(0)
    
    # Get/Set tiletype from within chunk
    def get(self, _tindex):
        return self.contents[_tindex.x][_tindex.y]
    def set_to(self, _tindex, val):
        self.contents[_tindex.x][_tindex.y] = val
        self.image.blit(
            tiles[self.get(_tindex)].sprite, # sprite in tile _tindex
            (
                _tindex.x * TILE_SIZE,
                _tindex.y * TILE_SIZE
            )
        )

# This class stores info on TYPE, not any particular tile
class Tile:
    def __init__(self, _name, _coll):
        self.name = _name           # Name, doubling as sprite index
        self.sprite = assets[_name]
        self.coll = _coll           # Physical properties

class Tilemap:
    def __init__(self):
        self.chunks = {}
        self.go = False
    
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
        #area is a Rect, sur a Surface
        #ix, iy iterate over places where chunk need to be rendered (bottom-right)
        for ix in range(area.x, area.x + area.width + int(CHUNK_SCRSIZE/DISPLAY_FACTOR), int(CHUNK_SCRSIZE*DISPLAY_FACTOR)):
            for iy in range(area.y, area.y + area.height + int(CHUNK_SCRSIZE/DISPLAY_FACTOR), int(CHUNK_SCRSIZE*DISPLAY_FACTOR)):
                sur.blit(
                    self.getchunk(XY(ix, iy) // CHUNK_SCRSIZE).image,
                    (
                        (ix - area.x - (area.x % CHUNK_SCRSIZE)) / DISPLAY_FACTOR,
                        (iy - area.y - (area.y % CHUNK_SCRSIZE)) / DISPLAY_FACTOR
                    )
                )
            
    def tocamera(self, cam):
        # ix, iy are chunk-coords
        c0 = (XY(cam.rect.topleft) / CHUNK_PIXSIZE).intize()
        c1 = (XY(cam.rect.bottomright) / CHUNK_PIXSIZE).intize()
        for ix in range(c0.x - 1, c1.x + 1):
            for iy in range(c0.y - 1, c1.y + 1):
                if self.go:
                    print (c1-c0)
                    self.go = False
                ixy = XY(ix, iy)
                cam.sur.blit(
                    self.getchunk(ixy).image,
                    (
                        cam.worldtoscreen(ixy * CHUNK_SCRSIZE * DISPLAY_FACTOR).totuple()
                    )
                )
        

# Convert point XY with epsilon data to tile XY index
def gettilefrompt(pt, eps=XY(0,0)):
    return [
        int(pt[0] // TILE_SIZE - (eps[0] < 0 and pt[0] % TILE_SIZE == 0)),
        int(pt[1] // TILE_SIZE - (eps[1] < 0 and pt[1] % TILE_SIZE == 0))
    ]
