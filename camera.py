from gameglobals import Game
from enginemath import XY
# from movable import Movable
import pygame


class Camera:
    def __init__(self, game: Game, _sur: pygame.Surface):
        """
        :param _sur: Surface the camera renders to
        """
        self.game = game
        
        self.sur = _sur
        self.sur.fill(pygame.Color("blue"))

        # rect in world coordinates
        self.rect = _sur.get_rect()
        self.rect.width *= self.game.quants_per_pixel
        self.rect.height *= self.game.quants_per_pixel
        print('Init\'d camera of size ' + repr(self.rect.size))

    # Convert between in-world and on-screen coordinates

    def worldtoscreen(self, xy: XY) -> XY:
        """Convert from in-world to on-screen coordinates."""
        return (xy - XY(self.rect.left, self.rect.top)) / self.game.quants_per_pixel

    def rectworldtoscreen(self, r: pygame.Rect) -> pygame.Rect:
        acc = r.copy()
        acc.width, acc.height = acc.width/self.game.quants_per_pixel, acc.height/self.game.quants_per_pixel
        acc.topleft = self.worldtoscreen(XY(r.left, r.top)).totuple()
        return acc

    def screentoworld(self, xy: XY) -> XY:
        """Convert from on-screen to in-world coordinates."""
        return xy * self.game.quants_per_pixel + XY(self.rect.left, self.rect.top)

    def updateposition(self):
        pass
