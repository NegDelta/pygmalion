class Game:
    tiles_per_chunk: int
    pixels_per_tile: int
    quants_per_pixel: int
    scroll_speed: int
    _assets: dict
    _tile_types: dict

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
        self._assets = {}
        self._tile_types = {}

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

    def register_asset(self):
        pass


TILES_PER_CHUNK = 12
PIXELS_PER_TILE = 16
QUANTS_PER_PIXEL = 20

QUANTS_PER_TILE = QUANTS_PER_PIXEL * PIXELS_PER_TILE
PIXELS_PER_CHUNK = TILES_PER_CHUNK * PIXELS_PER_TILE
QUANTS_PER_CHUNK = TILES_PER_CHUNK * QUANTS_PER_TILE

SCROLL_SPEED = 75 * QUANTS_PER_PIXEL

assets = {}
tiles = {}
