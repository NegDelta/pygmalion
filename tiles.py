from __future__ import annotations  # for the Game <-> tiles co-dependency
from pygame import Surface
from enginemath import XY
from typing import List, Callable

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gameglobals import Game


class Chunk:
    contents: List[List[int]]
    default_id = 0
    
    def __init__(self, game: Game, _index, *, mapgen: Callable):
        self.game = game
        self.index = _index
        self.contents = mapgen(self)
        self.image = Surface((int(game.pixels_per_chunk), int(game.pixels_per_chunk)))
        
        for ix in range(0, game.tiles_per_chunk):
            for iy in range(0, game.tiles_per_chunk):
                try:
                    self.image.blit(
                        game.tile_types[self.get(XY(ix, iy))].sprite,  # sprite in tile i
                        (
                            ix * game.quants_per_tile / game.quants_per_pixel,
                            iy * game.quants_per_tile / game.quants_per_pixel
                        )
                    )
                except TypeError:
                    print(self.contents[ix])
                    raise

    # Get/Set tiletype from within chunk
    def get(self, _tindex) -> int:
        return self.contents[_tindex.x][_tindex.y]

    def set_to(self, _tindex, val):
        self.contents[_tindex.x][_tindex.y] = val
        self.image.blit(
            self.game.tiles[self.get(_tindex)].sprite,  # sprite in tile _tindex
            (
                _tindex.x * self.game.quants_per_tile,
                _tindex.y * self.game.quants_per_tile
            )
        )


class TileType:
    name: str
    sprite: Surface
    coll: bool

    def __init__(self, _name: str, *, sprite: Surface, collides: bool):
        """
        :param _name: Identifier, also filename for sprites
        :param collides: Whether collisions occur
        """
        self.name = _name
        self.sprite = sprite
        self.coll = collides


class Tilemap:
    chunks: dict

    def __init__(self, game: Game, chunkgen: Callable):
        self.chunks = {}
        self.chunk_generator = chunkgen
        self.game = game
    
    # Get/Set tiletype of a single tile from within a tilemap
    def get(self, _tindex) -> int:
        if type(_tindex) != XY:
            _tindex = XY(_tindex[0], _tindex[1])
        cindex = _tindex // self.game.tiles_per_chunk
        tindex = _tindex % self.game.tiles_per_chunk
        return self.getchunk(cindex).get(tindex)

    def set_to(self, _tindex, val):
        if type(_tindex) != XY:
            _tindex = XY(_tindex[0], _tindex[1])
        cindex = _tindex // self.game.tiles_per_chunk
        tindex = _tindex % self.game.tiles_per_chunk
        self.getchunk(cindex).set_to(tindex, val)
    
    # Get a single chunk from within a tilemap
    def getchunk(self, _cindex):
        if not (_cindex.totuple()) in self.chunks.keys():
            self.chunks[_cindex.totuple()] = Chunk(self.game, _cindex, mapgen=self.chunk_generator)
        return self.chunks[_cindex.totuple()]
        
    def tocamera(self, cam):
        """Render a given area of tiles onto a camera's surface"""
        # ix, iy are chunk-coords
        c0 = (XY(cam.rect.left, cam.rect.top) / self.game.quants_per_chunk).intize()
        c1 = (XY(cam.rect.right, cam.rect.bottom) / self.game.quants_per_chunk).intize()
        for ix in range(c0.x - 1, c1.x + 1):
            for iy in range(c0.y - 1, c1.y + 1):
                ixy = XY(ix, iy)
                # point on screen where chunk is rendered
                scr_targetxy = cam.worldtoscreen(
                    ixy * self.game.quants_per_chunk
                ).floor()
                cam.sur.blit(self.getchunk(ixy).image, scr_targetxy.totuple())
