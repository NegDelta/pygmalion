import os

from pygame import Surface, image
from typing import Dict, Callable

from pygame.time import Clock

from tiles import TileType


class Game:
    tiles_per_chunk: int
    pixels_per_tile: int
    quants_per_pixel: int
    scroll_speed: int
    assets: Dict[str, Surface]
    tile_types: list
    tiles: dict
    on_tick: Callable[["Game"], None]

    def __init__(
            self, *,
            tiles_per_chunk,
            pixels_per_tile,
            quants_per_pixel,
            scroll_speed,
    ):
        self.movables = {}
        self.cameras = {}
        self.tilemaps = {}
        self.quants_per_pixel = quants_per_pixel
        self.pixels_per_tile = pixels_per_tile
        self.quants_per_tile = self.quants_per_pixel * self.pixels_per_tile
        self.tiles_per_chunk = tiles_per_chunk
        self.pixels_per_chunk = self.pixels_per_tile * self.tiles_per_chunk
        self.quants_per_chunk = self.quants_per_tile * self.tiles_per_chunk

        self.scroll_speed = scroll_speed
        self.assets = {}
        self.tiles = {}
        # self.tile_types = {0: pgtiles.TileType(_name="sky", collides=False)}
        self.tile_types = []

        self.clock = Clock()

    def register_tiletype(self, asset_key: str, collides: bool) -> int:
        """
        Register tiletype
        :return: The id of registered tiletype
        """
        new_type = TileType(asset_key, sprite=self.assets[asset_key], collides=collides)
        self.tile_types.append(new_type)
        new_index = len(self.tile_types) - 1
        return new_index

    def register_asset(self, key: str, filename: str):
        if key in self.assets.keys():
            raise ValueError("An asset is already registered at the key \"{}\"".format(key))
        script_dir = os.path.dirname(__file__)
        new_sprite: Surface = image.load(os.path.join(script_dir, 'assets', filename))
        self.assets[key] = new_sprite

    def register_object(self, key, obj):
        from tiles import Tilemap
        from movable import Movable
        from camera import Camera
        if isinstance(obj, Tilemap):
            target_dict = self.tilemaps
        elif isinstance(obj, Movable):
            target_dict = self.movables
        elif isinstance(obj, Camera):
            target_dict = self.cameras
        else:
            raise TypeError("Type {} cannot be registered as pygmalion object".format(type(obj)))
        target_dict: Dict
        if key in target_dict.keys():
            raise KeyError("Key {} is already registered".format(key))
        target_dict[key] = obj
        return obj

    def run(self):
        while True:
            self.on_tick(self)
