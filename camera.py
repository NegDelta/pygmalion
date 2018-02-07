from tiles import *

# TODO: isolate stuck-to-player camera as subclass
class Camera:
    def __init__(self, _sur, _mov):
        self.sur = _sur
        self.sur.fill(pygame.Color(0,0,255))
        self.mov = _mov
        
        # rect in world coordinates
        self.rect = _sur.get_rect()
        self.rect.width *= DISPLAY_FACTOR
        self.rect.height *= DISPLAY_FACTOR
        print(self.rect.size)
        
    def worldtoscreen(self, xy):
        return (xy - XY(self.rect.topleft)) / DISPLAY_FACTOR
        #return xy / DISPLAY_FACTOR - XY(self.rect.topleft)
        
    def screentoworld(self, xy):
        return xy * DISPLAY_FACTOR + XY(self.rect.topleft)
        #return (xy + XY(self.rect.topleft)) * DISPLAY_FACTOR
    
    def render(self):
        pass
        
    def update(self):
        self.rect.center = self.mov.center.totuple()
        self.render()