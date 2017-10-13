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
    
    #tx0 += getborder(x1-x0)
    #tx1 += getborder(x1-x0)
    #ty0 += getborder(y1-y0)
    #ty1 += getborder(y1-y0)    
    
    # [1] [ ] [ ] [0] [ ] [ ] [1]
    #  itx itx itx     itx itx itx
    #    ix  ix  ix  ix  ix  ix     
    
    collisiontiles = []
    # looping over tile indices
    if y1 != y0:
        # print('y range',y0,y1)
        for ity in range(ty0, ty1, sgn(y1-y0)): # vertical
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
            
    if x1 != x0:
        # print('x range',x0,x1)
        for itx in range(tx0, tx1, sgn(x1-x0)): # horizontal
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
    
    #tiles to check
    global markers
    markers += (map(lambda x:[x['tx']*16+8,x['ty']*16+8], collisiontiles))
    
    collisiontiles = sorted(collisiontiles, key = lambda x:x['k'])
    for itile in collisiontiles:
        pass #check bordering tile for collision
        if tiles[tmap.get(itile['tx'],itile['ty'])].coll:
            final_k = itile['k']
            break
    else:
        final_k = 1
    return final_k

pygame.init()

#load assets
assets['block'] = pygame.image.load(os.path.join('assets', 'block.png'))
assets['sky'] = pygame.image.load(os.path.join('assets', 'sky2.png'))
assets['marker'] = pygame.image.load(os.path.join('assets', 'marker.png'))
assets['marker-w'] = pygame.image.load(os.path.join('assets', 'marker-w.png'))
tiles[0] = Tile('sky', False)
tiles[1] = Tile('block', True)

worldmap = Tilemap()
velo = [0,0]
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
                print("eps",player.epsx,player.epsy)
            
            # DEBUG wasd keys
            elif event.key == pygame.K_w:
                player.moveto(player.x, gettilefrompt(
                    [player.x   , player.y],
                    [player.epsx, player.epsy]
                )[1] * TILE_SIZE)
            elif event.key == pygame.K_s:
                player.moveto(player.x, gettilefrompt(
                    [player.x   , player.y],
                    [player.epsx, player.epsy]
                )[1] * TILE_SIZE + TILE_SIZE)
            elif event.key == pygame.K_d:
                player.moveto(
                    gettilefrompt(
                        [player.x   , player.y],
                        [player.epsx, player.epsy]
                    )[0] * TILE_SIZE + TILE_SIZE,
                    player.y
                )
            
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
            print(player.x, player.y)
            x0,y0 = player.x, player.y
            x1 = event.pos[0] + view.x
            y1 = event.pos[1] + view.y
            p_eps = [player.epsx, player.epsy]

            col_k = collide([x0,y0],[x1,y1],p_eps,worldmap)
            markers.append([ipol(x0,x1,col_k), ipol(y0,y1,col_k)])
            #markers.append([x1 - x1%16 + 8, y1 - y1%16 + 8])
    
    displace[0] += unitize(velo, SCROLL_SPEED * interval/1000)[0]
    displace[1] += unitize(velo, SCROLL_SPEED * interval/1000)[1]
    
    # collide
    col_k = collide(
        [player.x              , player.y              ],
        [player.x + displace[0], player.y + displace[1]],
        [player.epsx, player.epsy], worldmap
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
