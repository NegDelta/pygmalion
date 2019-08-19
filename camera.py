from tiles import *
from enginemath import XY
import pygame


# TODO: isolate stuck-to-player camera as subclass
class Camera:
    def __init__(self, _sur, _mov):
        self.sur = _sur
        self.sur.fill(pygame.Color("blue"))
        self.mov = _mov

        # rect in world coordinates
        self.rect = _sur.get_rect()
        self.rect.width *= QUANTS_PER_PIXEL
        self.rect.height *= QUANTS_PER_PIXEL
        print('Init\'d camera of size ' + repr(self.rect.size))

    # Convert between in-world and on-screen coordinates

    def worldtoscreen(self, xy: XY) -> XY:
        return (xy - XY(self.rect.left, self.rect.top)) / QUANTS_PER_PIXEL

    def rectworldtoscreen(self, r: pygame.Rect) -> pygame.Rect:
        acc = r.copy()
        acc.width, acc.height = acc.width/QUANTS_PER_PIXEL, acc.height/QUANTS_PER_PIXEL
        acc.topleft = self.worldtoscreen(XY(r.left, r.top)).totuple()
        return acc

    def screentoworld(self, xy: XY) -> XY:
        return xy * QUANTS_PER_PIXEL + XY(self.rect.left, self.rect.top)

    def updateposition(self):
        self.rect.center = self.mov.center.totuple()
