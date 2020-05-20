from gameglobals import *
from enginemath import XY
# from movable import Movable
import pygame


class Camera:
    def __init__(self, _sur: pygame.Surface):
        """
        :param _sur: Surface the camera renders to
        """
        self.sur = _sur
        self.sur.fill(pygame.Color("blue"))

        # rect in world coordinates
        self.rect = _sur.get_rect()
        self.rect.width *= QUANTS_PER_PIXEL
        self.rect.height *= QUANTS_PER_PIXEL
        print('Init\'d camera of size ' + repr(self.rect.size))

    # Convert between in-world and on-screen coordinates

    def worldtoscreen(self, xy: XY) -> XY:
        """Convert from in-world to on-screen coordinates."""
        return (xy - XY(self.rect.left, self.rect.top)) / QUANTS_PER_PIXEL

    def rectworldtoscreen(self, r: pygame.Rect) -> pygame.Rect:
        acc = r.copy()
        acc.width, acc.height = acc.width/QUANTS_PER_PIXEL, acc.height/QUANTS_PER_PIXEL
        acc.topleft = self.worldtoscreen(XY(r.left, r.top)).totuple()
        return acc

    def screentoworld(self, xy: XY) -> XY:
        """Convert from on-screen to in-world coordinates."""
        return xy * QUANTS_PER_PIXEL + XY(self.rect.left, self.rect.top)

    def updateposition(self):
        pass
