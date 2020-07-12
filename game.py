# import os
import random
import sys
from typing import List
import pygame

# locals
from gameglobals import Game
from movable import Movable, MovableFollowingCamera
import tiles as pygm_tiles
from enginemath import *


# MAIN CODE BEGINS HERE #######


# initialize globals

pygame.init()
pygame.display.init()
screen = pygame.display.set_mode((640, 480))

game = Game(tiles_per_chunk=12, pixels_per_tile=16, quants_per_pixel=20, scroll_speed=1500)

print("TILES_PER_CHUNK =", game.tiles_per_chunk)
print("PIXELS_PER_TILE =", game.pixels_per_tile)
print("QUANTS_PER_PIXEL =", game.quants_per_pixel)

print("QUANTS_PER_TILE =", game.quants_per_tile)
print("PIXELS_PER_CHUNK =", game.pixels_per_chunk)
print("QUANTS_PER_CHUNK =", game.quants_per_chunk)

# load assets
game.register_asset('sky', 'sky.png')
game.register_asset('block', 'block.png')
TILE_SKY = game.register_tiletype('sky', False)
TILE_BLOCK = game.register_tiletype('block', True)


def dummy_gradient_chunkgen(c: pygm_tiles.Chunk) -> List[List[int]]:
    if c.index.y < 0:
        acc = [[0] * game.tiles_per_chunk] * game.tiles_per_chunk
    elif c.index.y > 0:
        acc = [[1] * game.tiles_per_chunk] * game.tiles_per_chunk
    else:
        acc = []
        for i in range(0, game.tiles_per_chunk):
            acc.append([])
            for j in range(0, game.tiles_per_chunk):
                if j / game.tiles_per_chunk > random.random():
                    acc[i].append(1)
                else:
                    acc[i].append(0)
    return acc


game.register_object("worldmap", pygm_tiles.Tilemap(game, dummy_gradient_chunkgen))
game.register_object("player", Movable(
    game, (0 * game.quants_per_pixel, 0, game.quants_per_tile, game.quants_per_tile),
    spriteid='marker', mapvelo=game.scroll_speed / 1000, weight=None
))
game.register_object("main", MovableFollowingCamera(game, screen, game.movables["player"]))

pygame.display.flip()
interval = 0
while True:
    interval = game.clock.tick(60)  # how much time elapsed since last frame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        # keypresses
        elif event.type == pygame.KEYDOWN:

            # DEBUG space
            if event.key == pygame.K_SPACE:
                # print("Your Xs: {} -- {}".format(player.left, player.right))
                # print("Your Ys: {} -- {}".format(player.top,  player.bottom))

                print("Ticks: {}".format(interval))

            elif event.key == pygame.K_ESCAPE:
                sys.exit()

        # DEBUG
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pass

    # poll arrow keys for movement
    pressed_keys = pygame.key.get_pressed()
    new_velo = XY(0, 0)
    if pressed_keys[pygame.K_LEFT]:
        new_velo += XY(-1, 0)
    if pressed_keys[pygame.K_DOWN]:
        new_velo += XY(0, 1)
    if pressed_keys[pygame.K_UP]:
        new_velo += XY(0, -1)
    if pressed_keys[pygame.K_RIGHT]:
        new_velo += XY(1, 0)
    game.movables["player"].velo = new_velo

    displace = game.movables["player"].get_collided_displace(
        game.scroll_speed * interval/1000, game.tilemaps["worldmap"]
    )
    game.movables["player"].move(displace)

    game.cameras["main"].updateposition()
    game.tilemaps["worldmap"].tocamera(game.cameras["main"])
    game.movables["player"].tocamera(game.cameras["main"])

    pygame.display.flip()

# and then close the whole thing
