from gameglobals import *
from enginemath import *

# TODO: rewrite to allow XY arguments

class Movable:
    def __init__(self, _x, _y, _w, _h, _spriteid, _weight=0):
        self.left = _x - _w / 2
        self.top = _y - _h / 2
        self.right = _x + _w / 2
        self.bottom = _y + _h / 2
        self.center = XY(_x, _y)
        self.size = XY(_w, _h)
        self.spriteid = _spriteid
        self.eps = XY(0,0)
        self.weight = _weight
        self.velo = XY(0.0, 0.0)

    def moveepsx(self, d):
        if d != 0:
            self.eps.x = -sgn(d)
    def moveepsy(self, d):
        if d != 0:
            self.eps.y = -sgn(d)

    # Motion methods, akin to pygame.Rect
    
    def setleft(self,a):
        d = a - self.left
        self.left += d
        self.right += d
        self.center.x += d
        self.moveepsx(d)
    def setright(self,a):
        d = a - self.right
        self.left += d
        self.right += d
        self.x += d
        self.moveepsx(d)
        
    def settop(self,a):
        d = a - self.top
        self.top += d
        self.bottom += d
        self.center.y += d
        self.moveepsy(d)
    def setbottom(self,a):
        d = a - self.bottom
        self.top += d
        self.bottom += d
        self.center.y += d
        self.moveepsy(d)
 
    def move(self,dx,dy):
        self.center.x += dx
        self.center.y += dy
        self.left += dx
        self.top += dy
        self.right += dx
        self.bottom += dy
        self.moveepsx(dx)
        self.moveepsy(dy)
        
    def render(self,area,sur):
        sur.blit(
            assets[self.spriteid],
            (
                self.left - area.x,
                self.top - area.y
            )
        )
