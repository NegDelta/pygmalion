# import pygame
import math
# from gameglobals import *
from enginemath import *
from tiles import *
from camera import Camera


# TODO: rewrite to allow XY arguments
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
        """
        Renders itself onto given camera
        """
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

    def get_collision(self, tmap: Tilemap, d: XY) -> XY:
        """
        Return actual displacement given map of obstacles
        :param tmap: Tilemap of obstacles
        :param d: Target displacement
        :return: Displacement ending at nearest obstacle
        """
        # TODO: replace k with final position at which collision occurs
        def collide(p0, p1):
            """Calculate the point at which movement between two points stops."""
            # p = x,y (0-1) -- current and target positions
            borderxy = XY(getborder((p1 - p0).x), getborder((p1 - p0).y))
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
                for ity in range(ty0, ty1, sgn(y1 - y0)):
                    y_iy = (ity + borderxy.y) * QUANTS_PER_TILE - borderxy.y
                    k = rev_ipol(y0, y1, y_iy)

                    y_ix = int(ipol(x0, x1, k))
                    tx = gettilefrompt([y_ix, y_iy])[0]
                    ty = ity + sgn(y1 - y0)

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
                for itx in range(tx0, tx1, sgn(x1 - x0)):
                    x_ix = (itx + borderxy.x) * QUANTS_PER_TILE - borderxy.x
                    k = rev_ipol(x0, x1, x_ix)
                    # if it's collided earlier, we're done
                    if k > terminalpos['k']:
                        break
                    x_iy = int(ipol(y0, y1, k))
                    tx = itx + sgn(x1 - x0)
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

        edges = list()

        # corners
        edges.append(XY(self.left, self.top))
        edges.append(XY(self.left, self.bottom - 1))
        edges.append(XY(self.right - 1, self.top))
        edges.append(XY(self.right - 1, self.bottom - 1))

        # points along the edges, just enough to have at least one on each tile
        # Edge cases would fit there just as well, but the less flops the better
        x_range = math.ceil(self.size.x / QUANTS_PER_TILE)
        for i in range(1, x_range):
            ix = int(ipol(self.left, self.right, i / x_range))
            edges.append(XY(ix, self.top))
            edges.append(XY(ix, self.bottom - 1))

        y_range = math.ceil(self.size.y / QUANTS_PER_TILE)
        for i in range(1, y_range):
            iy = int(ipol(self.top, self.bottom, i / y_range))
            edges.append(XY(self.left, iy))
            edges.append(XY(self.right - 1, iy))

        col_k = min(map(
            lambda edge: collide(edge, edge + d), edges
        ))
        d *= col_k
        d.intize()
        
        return d


class MovableFollowingCamera(Camera):
    def __init__(self, _sur: pygame.Surface, _mov: Movable):
        """
        :param _sur: Surface the camera renders to
        :param _mov: Movable the camera follows
        """

        super().__init__(_sur)
        self.mov = _mov

    def updateposition(self):
        self.rect.center = self.mov.center.totuple()
