import pygame
from gameglobals import *
# from enginemath import *


# TODO: rewrite to allow XY arguments
# TODO: consider ditching in favor of pygame.Rect
#       (but what about XY)
class Movable:
    def __init__(self, _x, _y, _w, _h, _spriteid, _weight=0):
        self.left = _x
        self.top = _y
        self.right = _x + _w
        self.bottom = _y + _h
        self.center = XY(_x, _y)
        self.size = XY(_w, _h)
        self.spriteid = _spriteid
        self.weight = _weight
        self.velo = XY(0, 0)

    # Motion methods, akin to pygame.Rect
    
    def setleft(self, a):
        d = a - self.left
        self.left += d
        self.right += d
        self.center.x += d

    def setright(self, a):
        d = a - self.right
        self.left += d
        self.right += d
        self.center.x += d
        
    def settop(self, a):
        d = a - self.top
        self.top += d
        self.bottom += d
        self.center.y += d

    def setbottom(self, a):
        d = a - self.bottom
        self.top += d
        self.bottom += d
        self.center.y += d
 
    def move(self, dx, dy):
        self.center.x += dx
        self.center.y += dy
        self.left += dx
        self.top += dy
        self.right += dx
        self.bottom += dy
    
    def get_rect(self):
        return pygame.Rect(self.left, self.top, self.size.x, self.size.y)
        
    def tocamera(self, cam):
        pygame.draw.rect(
            cam.sur, pygame.Color("white"),
            cam.rectworldtoscreen(self.get_rect())
        )
        '''cam.sur.blit(
            assets[self.spriteid],
            (
                cam.worldtoscreen(XY(self.left, self.top)).totuple()
            )
        )'''
