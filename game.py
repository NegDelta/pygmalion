import os
import sys
# import pygame
# import math  # for collision code
# from pygame.locals import *

# locals
# from gameglobals import *
# from enginemath import *
# from tiles import *
from movable import *
from camera import *


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
tiles[0] = Tile('sky', False)
tiles[1] = Tile('block', True)


worldmap = Tilemap()
masterclk, interval = pygame.time.get_ticks(), 0

player = Movable(0, 0, QUANTS_PER_TILE, QUANTS_PER_TILE, 'marker')

pygame.display.init()
screen = pygame.display.set_mode((640, 480))
view = screen.get_rect()
view.w *= QUANTS_PER_PIXEL
view.h *= QUANTS_PER_PIXEL

camera = MovableFollowingCamera(screen, player)

pygame.display.flip()
clk = pygame.time.Clock()

while True:
    displace = XY(0, 0)  # of the player, TODO: move to Movable
    interval = clk.tick()  # how much time elapsed since last frame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        # keypresses
        elif event.type == pygame.KEYDOWN:
            # TODO: switch to polling arrow keys
            # arrow keys - add movement
            if event.key == pygame.K_LEFT:
                player.velo = diradd(player.velo, [-1, 0])
            if event.key == pygame.K_DOWN:
                player.velo = diradd(player.velo, [0, 1])
            if event.key == pygame.K_UP:
                player.velo = diradd(player.velo, [0, -1])
            if event.key == pygame.K_RIGHT:
                player.velo = diradd(player.velo, [1, 0])

            # DEBUG space
            elif event.key == pygame.K_SPACE:
                worldmap.go = True
                print("Your Xs: {} -- {}".format(player.left, player.right))
                print("Your Ys: {} -- {}".format(player.top,  player.bottom))

            elif event.key == pygame.K_ESCAPE:
                sys.exit()

        # TODO: switch to polling arrow keys
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.velo = dirsub(player.velo, [-1, 0])
            if event.key == pygame.K_DOWN:
                player.velo = dirsub(player.velo, [0, 1])
            if event.key == pygame.K_UP:
                player.velo = dirsub(player.velo, [0, -1])
            if event.key == pygame.K_RIGHT:
                player.velo = dirsub(player.velo, [1, 0])
                
        # DEBUG
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pass
    
    displace += unitize(player.velo, SCROLL_SPEED * interval/1000)
    displace.intize()
    
    # collide
    col_displace = player.get_collision(worldmap, displace)

    player.move(col_displace.x, col_displace.y)
    
    camera.updateposition()
    worldmap.tocamera(camera)
    player.tocamera(camera)
    
    pygame.display.flip()

# and then close the whole thing
