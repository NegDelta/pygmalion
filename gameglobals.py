import os

from pygame import Surface, image
from typing import Dict


class Game:
    tiles_per_chunk: int
    pixels_per_tile: int
    quants_per_pixel: int
    scroll_speed: int
    assets: Dict[str, Surface]
    tile_types: dict

    def __init__(
            self, *,
            tiles_per_chunk,
            pixels_per_tile,
            quants_per_pixel,
            scroll_speed,
    ):
        self.tiles_per_chunk = tiles_per_chunk
        self.pixels_per_tile = pixels_per_tile
        self.quants_per_pixel = quants_per_pixel
        self.scroll_speed = scroll_speed
        self.assets = {}
        # self.tile_types = {0: TileType(_name="sky", collides=False)}

    def quants_per_tile(self):
        return self.quants_per_pixel * self.pixels_per_tile

    def quants_per_chunk(self):
        return self.quants_per_tile() * self.tiles_per_chunk

    def pixels_per_chunk(self):
        return self.pixels_per_tile * self.tiles_per_chunk

    def register_tiletype(self) -> int:
        """
        Register tiletype
        :return: The id of registered tiletype
        """
        pass

    def register_asset(self, key: str, filename: str):
        if key in self.assets.keys():
            raise ValueError("An asset is already registered at the key \"{}\"".format(key))
        script_dir = os.path.dirname(__file__)
        self.assets[key] = image.load(os.path.join(script_dir, 'assets', filename))


TILES_PER_CHUNK = 12
PIXELS_PER_TILE = 16
QUANTS_PER_PIXEL = 20

QUANTS_PER_TILE = QUANTS_PER_PIXEL * PIXELS_PER_TILE
PIXELS_PER_CHUNK = TILES_PER_CHUNK * PIXELS_PER_TILE
QUANTS_PER_CHUNK = TILES_PER_CHUNK * QUANTS_PER_TILE

SCROLL_SPEED = 75 * QUANTS_PER_PIXEL

assets: Dict[str, Surface] = {}
tiles: dict = {}
