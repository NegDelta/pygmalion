import os
import random
import sys

import pygame

from movable import Movable, MovableFollowingCamera
# locals
# from gameglobals import *
# from enginemath import *
from tiles import *

# import math  # for collision code
# from pygame.locals import *
# from camera import Camera


# MAIN CODE BEGINS HERE #######


# initialize globals
print("TILES_PER_CHUNK =", TILES_PER_CHUNK)
print("PIXELS_PER_TILE =", PIXELS_PER_TILE)
print("QUANTS_PER_PIXEL =", QUANTS_PER_PIXEL)

print("QUANTS_PER_TILE =", QUANTS_PER_TILE)
print("PIXELS_PER_CHUNK =", PIXELS_PER_CHUNK)
print("QUANTS_PER_CHUNK =", QUANTS_PER_CHUNK)

# absolute dir the script is in, for relative paths
script_dir = os.path.dirname(__file__)

pygame.init()

# load assets
assets['block'] = pygame.image.load(os.path.join(script_dir, 'assets', 'block.png'))
assets['sky'] = pygame.image.load(os.path.join(script_dir, 'assets', 'sky.png'))
assets['marker'] = pygame.image.load(os.path.join(script_dir, 'assets', 'marker.png'))
assets['marker-w'] = pygame.image.load(os.path.join(script_dir, 'assets', 'marker-w.png'))
tiles[0] = TileType('sky', collides=False)
tiles[1] = TileType('block', collides=True)


def dummy_gradient_chunkgen(c: Chunk) -> List[List[int]]:
    if c.index.y < 0:
        acc = [[0] * TILES_PER_CHUNK] * TILES_PER_CHUNK
    elif c.index.y > 0:
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


worldmap = Tilemap(dummy_gradient_chunkgen)
masterclk, interval = pygame.time.get_ticks(), 0

player = Movable(
    (0 * QUANTS_PER_PIXEL, 0, QUANTS_PER_TILE, QUANTS_PER_TILE),
    spriteid='marker', mapvelo=SCROLL_SPEED/1000, weight=None
)

pygame.display.init()
screen = pygame.display.set_mode((640, 480))

camera = MovableFollowingCamera(screen, player)

pygame.display.flip()
clk = pygame.time.Clock()

while True:
    interval = clk.tick(60)  # how much time elapsed since last frame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        # keypresses
        elif event.type == pygame.KEYDOWN:

            # DEBUG space
            if event.key == pygame.K_SPACE:
                worldmap.go = True
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
    player.velo = new_velo

    displace = player.get_collided_displace(SCROLL_SPEED * interval/1000, worldmap)
    player.move(displace)

    camera.updateposition()
    worldmap.tocamera(camera)
    player.tocamera(camera)

    pygame.display.flip()

# and then close the whole thing
