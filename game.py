import os
import sys
# import pygame
import math  # for collision code
# from pygame.locals import *

# locals
# from gameglobals import *
# from enginemath import *
# from tiles import *
from movable import *
from camera import *


# TODO: replace k with final position at which collision occurs
def collide(p0, p1, tmap):
    """Calculate the point at which movement between two points stops."""
    # p = x,y (0-1) -- current and target positions
    borderxy = XY(getborder((p1-p0).x), getborder((p1-p0).y)) 
    # p0 -= borderxy
    # p1 -= borderxy
    x0, y0 = p0.totuple()
    x1, y1 = p1.totuple()
    # tx, ty (0-1) -- current and target tiles
    tx0, ty0 = gettilefrompt(p0)
    tx1, ty1 = gettilefrompt(p1)    

    terminalpos = {
        'x': x1, 'y': y1, 'k': 1,
        'tx': tx1,
        'ty': ty1
    }
    
    # ix,  iy  -- point coords
    # itx, ity -- tile  coords
    
    # collision from top/bottom
    if y1 != y0:
        for ity in range(ty0, ty1, sgn(y1-y0)):
            y_iy = (ity + borderxy.y) * QUANTS_PER_TILE - borderxy.y
            k = rev_ipol(y0, y1, y_iy)
            
            y_ix = int(ipol(x0, x1, k))
            tx = gettilefrompt([y_ix, y_iy])[0]
            ty = ity + sgn(y1-y0)
            
            # if it's a colliding tile, we're done at this axis
            if tiles[tmap.get(XY(tx, ty))].coll:
                terminalpos = {
                    'x': y_ix, 'y': y_iy, 'k': k,
                    'tx': tx,
                    'ty': ty
                }
                break
            
    # from left/right
    if x1 != x0:
        for itx in range(tx0, tx1, sgn(x1-x0)):
            x_ix = (itx + borderxy.x) * QUANTS_PER_TILE - borderxy.x
            k = rev_ipol(x0, x1, x_ix)
            # if it's collided earlier, we're done
            if k > terminalpos['k']:
                break
            x_iy = int(ipol(y0, y1, k))
            tx = itx + sgn(x1-x0)
            ty = gettilefrompt([x_ix, x_iy])[1]
            
            # if it's a colliding tile, we're done
            if tiles[tmap.get(XY(tx, ty))].coll:
                terminalpos = {
                    'x': x_ix, 'y': x_iy, 'k': k,
                    'tx': tx,
                    'ty': ty
                }
                break
    
    if terminalpos['k'] < 1:
        print("Collided at ", terminalpos)
        print(" from {} to {}".format(p0, p1))
    return terminalpos['k']
    
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
# player = Movable(0.0, 0.0, 5*QUANTS_PER_PIXEL, 5*QUANTS_PER_PIXEL, 'marker')

pygame.display.init()
screen = pygame.display.set_mode((640, 480))
view = screen.get_rect()
view.w *= QUANTS_PER_PIXEL
view.h *= QUANTS_PER_PIXEL

camera = Camera(screen, player)

pygame.display.flip()
clk = pygame.time.Clock()

while True:
    displace = XY(0, 0)
    interval = clk.tick()
    markers = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        # keypresses
        elif event.type == pygame.KEYDOWN:
            # TODO: relegate to Controls or MoveMech
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
            
        elif event.type == pygame.KEYUP:
            # TODO: relegate to Controls or MoveMech
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
    edges = list()
    
    # corners
    edges.append(XY(player.left,    player.top))
    edges.append(XY(player.left,    player.bottom-1))
    edges.append(XY(player.right-1, player.top))
    edges.append(XY(player.right-1, player.bottom-1))
    
    # points along the edges, just enough to have at least one on each tile
    # Edge cases would fit there just as well, but the less flops the better
    # TODO: apparently these don't show up
    x_range = math.ceil(player.size.x / QUANTS_PER_TILE)
    for i in range(1, x_range):
        ix = int(ipol(player.left, player.right, i/x_range))
        edges.append(XY(ix, player.top))
        edges.append(XY(ix, player.bottom-1))
        
    y_range = math.ceil(player.size.y / QUANTS_PER_TILE)
    for i in range(1, y_range):
        iy = int(ipol(player.top, player.bottom, i/y_range))
        edges.append(XY(player.left,    iy))
        edges.append(XY(player.right-1, iy))
    
    col_k = min(map(
        lambda edge: collide(
            edge, edge + displace, worldmap
        ), edges
    ))
    displace *= col_k
    displace.intize()
    player.move(displace.x, displace.y)
    
    camera.updateposition()
    worldmap.tocamera(camera)
    player.tocamera(camera)
    
    pygame.display.flip()

# and then close the whole thing
