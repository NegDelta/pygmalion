import os,sys
import pygame
import math # for collision code
from pygame.locals import *

#locals
from gameglobals import *
from enginemath import *
from tiles import *
from movable import *
from camera import *

def collide(p0, p1, eps, tmap):
    x0, y0 = p0.totuple()
    x1, y1 = p1.totuple()
    
    tx0, ty0 = gettilefrompt(p0, eps)
    tx1, ty1 = gettilefrompt(p1)    
    
    # tiles to be checked for collision
    collisiontiles = []
    
    # ix,  iy  -- point coords
    # itx, ity -- tile  coords
    
    # collision from top/bottom
    if y1 != y0:
        for ity in range(ty0, ty1, sgn(y1-y0)):
            iy = (ity + getborder(y1-y0)) * QUANTS_PER_TILE
            k = rev_ipol(y0, y1, iy)
            ix = ipol(x0, x1, k)
            tx = gettilefrompt([ix,iy],eps)[0]
            ty = ity + sgn(y1-y0)
            collisiontiles.append({
                'x': ix, 'y': iy, 'k': k,
                'tx': tx,
                'ty': ty
            })
            
    # from left/right
    if x1 != x0:
        for itx in range(tx0, tx1, sgn(x1-x0)):
            ix = (itx + getborder(x1-x0)) * QUANTS_PER_TILE
            k = rev_ipol(x0, x1, ix)
            iy = ipol(y0, y1, k)
            tx = itx + sgn(x1-x0)
            ty = gettilefrompt([ix,iy],eps)[1]
            collisiontiles.append({
                'x': ix, 'y': iy, 'k': k,
                'tx': tx,
                'ty': ty
            })
    
    # sort collisiontiles by k, i.e. order of getting hit
    collisiontiles = sorted(collisiontiles, key = lambda x:x['k'])
    
    for itile in collisiontiles:
        # check bordering tile for collision
        if tiles[tmap.get(XY(itile['tx'],itile['ty']))].coll:
            final_k = itile['k']
            break
    else:
        final_k = 1
    return final_k
    
####################### MAIN CODE BEGINS HERE #######

# initialize globals

# absolute dir the script is in, for relative paths
script_dir = os.path.dirname(__file__)

pygame.init()

#load assets
assets['block'] = pygame.image.load\
                  (os.path.join(script_dir, 'assets', 'block.png'))
assets['sky'] = pygame.image.load\
                  (os.path.join(script_dir, 'assets', 'sky.png'))
assets['marker'] = pygame.image.load\
                  (os.path.join(script_dir, 'assets', 'marker.png'))
assets['marker-w'] = pygame.image.load\
                  (os.path.join(script_dir, 'assets', 'marker-w.png'))
tiles[0] = Tile('sky', False)
tiles[1] = Tile('block', True)


worldmap = Tilemap()
masterclk, interval = pygame.time.get_ticks(), 0

player = Movable(0.0, 0.0, 200, 200, 'marker')

pygame.display.init()
screen = pygame.display.set_mode((640, 480))
view = screen.get_rect()
view.w *= QUANTS_PER_PIXEL
view.h *= QUANTS_PER_PIXEL

camera = Camera(screen, player)

pygame.display.flip()
clk = pygame.time.Clock()

while True:
    displace = XY(0.0, 0.0)
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
                player.velo = diradd(player.velo,[-1, 0])
            if event.key == pygame.K_DOWN:
                player.velo = diradd(player.velo,[ 0, 1])
            if event.key == pygame.K_UP:
                player.velo = diradd(player.velo,[ 0,-1])
            if event.key == pygame.K_RIGHT:
                player.velo = diradd(player.velo,[ 1, 0])
            
            # DEBUG space
            elif event.key == pygame.K_SPACE:
                worldmap.go = True
            
            elif event.key == pygame.K_ESCAPE:
                sys.exit()
            
        elif event.type == pygame.KEYUP:
            # TODO: relegate to Controls or MoveMech
            if event.key == pygame.K_LEFT:
                player.velo = dirsub(player.velo,[-1, 0])
            if event.key == pygame.K_DOWN:
                player.velo = dirsub(player.velo,[ 0, 1])
            if event.key == pygame.K_UP:
                player.velo = dirsub(player.velo,[ 0,-1])
            if event.key == pygame.K_RIGHT:
                player.velo = dirsub(player.velo,[ 1, 0])
                
        # DEBUG
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(repr(event))
            mousexy = XY(event.pos)
            viewxy = XY(view.center)
            realxy = mousexy + viewxy
            print('mousexy:', mousexy)
            print('viewxy:', viewxy)
            print('realxy:', realxy)
            de_tile = gettilefrompt(realxy)
            print('tile: ', de_tile)
            print('type: ', worldmap.get(de_tile))
            worldmap.t = True
    
    displace += unitize(player.velo, SCROLL_SPEED * interval/1000)
    
    # collide
    edges = list()
    
    # corners
    edges.append(XY(player.left,  player.top))
    edges.append(XY(player.left,  player.bottom))
    edges.append(XY(player.right, player.top))
    edges.append(XY(player.right, player.bottom))
    
    # points along the edges, just enough to have at least one on each tile
    # Edge cases would fit there just as well, but the less flops the better
    xrange = math.ceil(player.size.x / QUANTS_PER_TILE)
    for i in range(1, xrange-1):
        ix = ipol(player.left, player.right, i/xrange)
        edges.append(XY(ix, player.top))
        edges.append(XY(ix, player.bottom))
        
    yrange = math.ceil(player.size.y / QUANTS_PER_TILE)
    for i in range(1, yrange-1):
        iy = ipol(player.top, player.bottom, i/xrange)
        edges.append(XY(player.left,  iy))
        edges.append(XY(player.right, iy))
    
    col_k = min(map(lambda edge : collide(
        edge, edge + displace, player.eps, worldmap
    ), edges))
    
    player.move(displace[0] * col_k, displace[1] * col_k)
    
    camera.update()
    worldmap.tocamera(camera)
    player.tocamera(camera)
    
    pygame.display.flip()

#and then close the whole thing
