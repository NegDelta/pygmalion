# import pygame
import math
# from gameglobals import *
from enginemath import *
from tiles import *
from camera import Camera


class Movable:
    def __init__(self, coords, spriteid, weight, mapvelo):
        size = XY()

        if len(coords) == 4:  # Number, Number. Number, Number
            top, left, w, h = coords
            size = XY(w, h)
        elif len(coords) == 2:  # XY, XY
            topleft, size = coords
            top, left = topleft
        elif len(coords) == 3:
            if type(coords[1]) == XY:
                raise SyntaxError("Too many coordinates")
            else:
                if type(coords[0]) == XY and type(coords[2]) != XY:  # XY, Num, Num
                    topleft, w, h = coords
                    top, left = topleft
                elif type(coords[0]) != XY and type(coords[2]) == XY:  # Num, Num, XY
                    top, left, size = coords
                else:  # Num, Num, Num
                    raise SyntaxError("Not enough arguments")
        else:
            raise SyntaxError("Wrong number of arguments")
        self.left = left
        self.top = top
        self.size = size
        self.right = self.left + self.size.x
        self.bottom = self.top + self.size.y
        self.center = XY(top, left) + self.size/2
        self.spriteid = spriteid
        self.weight = weight
        self.velo = XY()
        self.mapvelo = mapvelo

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
 
    def move(self, d: XY):
        self.center.x += d.x
        self.center.y += d.y
        self.left += d.x
        self.top += d.y
        self.right += d.x
        self.bottom += d.y
    
    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.left, self.top, self.size.x, self.size.y)

    def get_raw_displace(self, dt) -> XY:
        acc = XY(self.velo)
        acc = acc.unitize(dt).intize()
        return acc

    def get_collided_displace(self, dt, tmap: Tilemap) -> XY:
        acc = self.get_raw_displace(dt)
        acc = self.get_collision(tmap, acc)
        return acc
        
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
        def collide(p0: XY, p1: XY) -> dict:
            """Calculate the point at which movement between two points stops."""
            # TODO: rewrite to use PotentialCollPoint instead of dict

            # p (0-1) -- current and target positions
            delta: XY = p1 - p0
            borderxy: XY = XY(getborder(delta.x), getborder(delta.y))

            # tx, ty (0-1) -- current and target tiles
            t0: XY = gettilefrompt(p0)
            t1: XY = gettilefrompt(p1)

            if t0 == t1:
                return {"k": 1, "p": p1}

            # print("Colliding from {} to {}".format(p0, p1))

            def get_tile_border(tile_coord, dirv):
                border_coord = (tile_coord + getborder(dirv)) * QUANTS_PER_TILE
                return border_coord

            def get_axis_isect(**kwargs) -> dict:
                """
                Return XY which intersects p0-p1 and a given axis parallel
                :param kwargs: coord either at x or y
                :return: XY with given x or y and the other coord computed
                """
                if 'x' in kwargs.keys():
                    c = "x"
                    given0, given1 = p0.x, p1.x
                elif 'y' in kwargs.keys():
                    c = "y"
                    given0, given1 = p0.y, p1.y
                else:
                    raise SyntaxError
                given = kwargs[c]
                k = rev_ipol(given0, given1, given)
                if c == 'x':
                    acc = XY(given, ipol(p0.y, p1.y, k))
                else:
                    acc = XY(ipol(p0.x, p1.x, k), given)
                acc = acc.intize()
                return {"p": acc, "k": k}

            def get_checks_from_tile_coord(**kwargs) -> dict:
                coll_tile = XY()
                if 'x' in kwargs.keys():
                    tile_x = kwargs["x"]
                    coll_tile.x = tile_x + sgn(delta.x)
                    y_axis_parallel = get_tile_border(tile_x, sgn(delta.x)) - getborder(delta.x)
                    isect = get_axis_isect(x=y_axis_parallel)
                    coll_tile.y = gettilefromcoord(isect["p"].y)
                elif 'y' in kwargs.keys():
                    tile_y = kwargs["y"]
                    coll_tile.y = tile_y + sgn(delta.y)
                    x_axis_parallel = get_tile_border(tile_y, sgn(delta.y)) - getborder(delta.y)
                    isect = get_axis_isect(y=x_axis_parallel)
                    coll_tile.x = gettilefromcoord(isect["p"].x)
                else:
                    raise SyntaxError
                acc = isect
                acc["t"] = coll_tile
                return acc

            def check_candidates():
                if delta.x != 0:
                    x_checks = list(map(
                        lambda x: get_checks_from_tile_coord(x=x),
                        range(floor(t0.x), floor(t1.x), sgn(delta.x))
                    ))
                else:
                    x_checks = []
                if delta.y != 0:
                    y_checks = list(map(
                        lambda y: get_checks_from_tile_coord(y=y),
                        range(floor(t0.y), floor(t1.y), sgn(delta.y))
                    ))
                else:
                    y_checks = []
                iter_x = iter(x_checks)
                iter_y = iter(y_checks)

                def safe_next(it):
                    try:
                        acc = next(it)
                        return acc
                    except StopIteration:
                        return None

                next_x = safe_next(iter_x)
                next_y = safe_next(iter_y)

                while next_x is not None or next_y is not None:
                    if next_x is None:
                        yield next_y
                        next_y = safe_next(iter_y)
                    elif next_y is None:
                        yield next_x
                        next_x = safe_next(iter_x)
                    else:
                        if next_x["k"] < next_y["k"]:
                            yield next_x
                            next_x = safe_next(iter_x)
                        else:
                            yield next_y
                            next_y = safe_next(iter_y)
                return  # check_candidates

            for candidate_pt in check_candidates():
                # print("Checking stop at {}".format(candidate_pt))
                check_tile = candidate_pt["t"]
                check_tiletype = tmap.get(check_tile)
                if tiles[check_tiletype].coll:
                    return candidate_pt

            return {"p": p1, "k": 1}

        edges = list()  # all points along the movable's rect which would be collided

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

        collided_edges = list(map(lambda edge: (edge, collide(edge, edge + d)), edges))
        # c_es are tuples (edge, dict("p", "k"))

        pess_collided_edge = min(collided_edges, key=lambda c_e: c_e[1]["k"])
        pess_delta = pess_collided_edge[1]["p"] - pess_collided_edge[0]

        return pess_delta


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
