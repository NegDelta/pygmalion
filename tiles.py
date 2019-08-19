import pygame
import random
from gameglobals import *
from enginemath import XY
from typing import List


# TODO: add support for partial initialization
class Chunk:
    default_id = 0
    
    def __init__(self, _index):
        self.index = _index
        self.contents = self.initmap()
        self.image = pygame.Surface((int(PIXELS_PER_CHUNK), int(PIXELS_PER_CHUNK)))
        
        for ix in range(0, TILES_PER_CHUNK):
            for iy in range(0, TILES_PER_CHUNK):
                try:
                    self.image.blit(
                        tiles[self.get(XY(ix, iy))].sprite,  # sprite in tile i
                        (
                            ix * QUANTS_PER_TILE / QUANTS_PER_PIXEL,
                            iy * QUANTS_PER_TILE / QUANTS_PER_PIXEL
                        )
                    )
                except TypeError:
                    print(self.contents[ix])
                    raise
                    
    def initmap(self) -> List[List[int]]:
        return self.initgrund()
    
    # Generators. TODO: isolate or move to main
    def initbaka(self) -> List[List[int]]:
        """
        Generates an "empty" chunk filled with default_id.
        :return: a 2d array of chunk contents
        """
        print('Generating chunk ', self.index)
        acc = []
        for i in range(0, TILES_PER_CHUNK):
            acc.append([[self.default_id] * TILES_PER_CHUNK])
        acc[1][1] = 1
        return acc

    def initgrund(self) -> List[List[int]]:
        print('Generating chunk ', self.index)
        if self.index.y < 0:
            acc = [[0] * TILES_PER_CHUNK] * TILES_PER_CHUNK
        elif self.index.y > 0:
            acc = [[1] * TILES_PER_CHUNK] * TILES_PER_CHUNK
        else:
            acc = []
            for i in range(0, TILES_PER_CHUNK):
                acc.append([])
                for j in range(0, TILES_PER_CHUNK):
                    if j / TILES_PER_CHUNK > random.random():
                        acc[i].append(1)
                    else:
                        acc[i].append(0)
        return acc
    
    # Get/Set tiletype from within chunk
    def get(self, _tindex):
        return self.contents[_tindex.x][_tindex.y]

    def set_to(self, _tindex, val):
        self.contents[_tindex.x][_tindex.y] = val
        self.image.blit(
            tiles[self.get(_tindex)].sprite,  # sprite in tile _tindex
            (
                _tindex.x * QUANTS_PER_TILE,
                _tindex.y * QUANTS_PER_TILE
            )
        )


# This class stores info on TYPE, not any particular tile
class Tile:
    def __init__(self, _name: str, _coll: bool):
        """
        :param _name: Identifier, also filename for sprites
        :param _coll: Whether collisions occur
        """
        self.name = _name
        self.sprite = assets[_name]
        self.coll = _coll


class Tilemap:
    chunks: dict
    go: bool

    def __init__(self):
        self.chunks = {}
        self.go = False
    
    # Get/Set tiletype of a single tile from within a tilemap
    def get(self, _tindex):
        if type(_tindex) != XY:
            _tindex = XY(_tindex[0], _tindex[1])
        cindex = _tindex // TILES_PER_CHUNK
        tindex = _tindex % TILES_PER_CHUNK
        return self.getchunk(cindex).get(tindex)

    def set_to(self, _tindex, val):
        if type(_tindex) != XY:
            _tindex = XY(_tindex[0], _tindex[1])
        cindex = _tindex // TILES_PER_CHUNK
        tindex = _tindex % TILES_PER_CHUNK
        self.getchunk(cindex).set_to(tindex, val)
    
    # Get a single chunk from within a tilemap
    def getchunk(self, _cindex):
        if not (_cindex.totuple()) in self.chunks.keys():
            self.chunks[_cindex.totuple()] = Chunk(_cindex)
        return self.chunks[_cindex.totuple()]
        
    # Render a given area of tiles onto a camera's surface            
    def tocamera(self, cam):
        # ix, iy are chunk-coords
        c0 = (XY(cam.rect.left, cam.rect.top) / QUANTS_PER_CHUNK).intize()
        c1 = (XY(cam.rect.right, cam.rect.bottom) / QUANTS_PER_CHUNK).intize()
        for ix in range(c0.x - 1, c1.x + 1):
            for iy in range(c0.y - 1, c1.y + 1):
                ixy = XY(ix, iy)
                # point on screen where chunk is rendered
                scr_targetxy = cam.worldtoscreen(
                    ixy * PIXELS_PER_CHUNK * QUANTS_PER_PIXEL  # QUANTS_PER_CHUNK
                ).floor()
                if self.go:
                    pass
                cam.sur.blit(self.getchunk(ixy).image, scr_targetxy.totuple())
        if self.go:
            pass
        self.go = False
        

# Convert point XY with epsilon data to tile XY index
def gettilefrompt(pt):
    return [
        int(pt[0] // QUANTS_PER_TILE),
        int(pt[1] // QUANTS_PER_TILE)
    ]
