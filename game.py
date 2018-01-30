import os,sys
import random
import pygame
from pygame.locals import *

#locals
from gameglobals import *
from enginemath import *
from tiles import *
from movable import *

def mark_point(area,sur,x,y):
    sur.blit(
        assets['marker'],
        (
            int(x) - area.x - 8,
            int(y) - area.y - 8
        )
    )

def collide(p0, p1, eps, tmap):
    x0, y0 = p0
    x1, y1 = p1
    
    tx0, ty0 = gettilefrompt(p0, eps)
    tx1, ty1 = gettilefrompt(p1)    
    
    # tiles to be checked for collision
    collisiontiles = []
    
    # ix,  iy  -- point coords
    # itx, ity -- tile  coords
    
    # collision from top/bottom
    if y1 != y0:
        for ity in range(ty0, ty1, sgn(y1-y0)):
            iy = (ity + getborder(y1-y0)) * TILE_SIZE
            k = rev_ipol(y0, y1, iy)
            ix = ipol(x0, x1, k)
            print('ver:',ix,iy)
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
            ix = (itx + getborder(x1-x0)) * TILE_SIZE
            k = rev_ipol(x0, x1, ix)
            iy = ipol(y0, y1, k)
            print('hor:',ix,iy)
            tx = itx + sgn(x1-x0)
            ty = gettilefrompt([ix,iy],eps)[1]
            collisiontiles.append({
                'x': ix, 'y': iy, 'k': k,
                'tx': tx,
                'ty': ty
            })
    
    # TODO: move to renderer
    # tiles to check
    global markers
    markers += (map(lambda x:[x['tx']*16+8,x['ty']*16+8], collisiontiles))
    
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
                  (os.path.join(script_dir, 'assets', 'sky2.png'))
assets['marker'] = pygame.image.load\
                  (os.path.join(script_dir, 'assets', 'marker.png'))
assets['marker-w'] = pygame.image.load\
                  (os.path.join(script_dir, 'assets', 'marker-w.png'))
tiles[0] = Tile('sky', False)
tiles[1] = Tile('block', True)


worldmap = Tilemap()
velo = [0,0] # TODO relegate to Movable object
masterclk, interval = pygame.time.get_ticks(), 0

player = Movable(0.0, 0.0, 16, 16, 'marker')

pygame.display.init()
screen = pygame.display.set_mode((640, 480))
view = screen.get_rect()

screen.fill(pygame.Color(0,0,255))
pygame.display.flip()
clk = pygame.time.Clock()

while True:
    displace = [0.0, 0.0]
    interval = clk.tick()
    markers = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        # keypresses
        elif event.type == pygame.KEYDOWN:
            # arrow keys - add movement
            if event.key == pygame.K_LEFT:
                velo = diradd(velo,[-1, 0])
            if event.key == pygame.K_DOWN:
                velo = diradd(velo,[ 0, 1])
            if event.key == pygame.K_UP:
                velo = diradd(velo,[ 0,-1])
            if event.key == pygame.K_RIGHT:
                velo = diradd(velo,[ 1, 0])
            
            # DEBUG space
            elif event.key == pygame.K_SPACE:
                print("Player",player.x, player.y)
                print("eps",player.eps.x,player.eps.y)
            
            elif event.key == pygame.K_ESCAPE:
                sys.exit()
            
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                velo = dirsub(velo,[-1, 0])
            if event.key == pygame.K_DOWN:
                velo = dirsub(velo,[ 0, 1])
            if event.key == pygame.K_UP:
                velo = dirsub(velo,[ 0,-1])
            if event.key == pygame.K_RIGHT:
                velo = dirsub(velo,[ 1, 0])
                
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
    
    displace[0] += unitize(velo, SCROLL_SPEED * interval/1000)[0]
    displace[1] += unitize(velo, SCROLL_SPEED * interval/1000)[1]
    
    # collide
    col_k = collide(
        [player.x              , player.y              ],
        [player.x + displace[0], player.y + displace[1]],
        [player.eps.x, player.eps.y], worldmap
    )
    
    player.move(displace[0] * col_k, displace[1] * col_k)
    view.x = player.x - 320
    view.y = player.y - 240
    
    worldmap.render(view, screen)
    for im in markers:
        pass#mark_point(view, screen, im[0], im[1])
    player.render(view, screen)
    
    pygame.display.flip()
    #print(interval)

#and then close the whole thing