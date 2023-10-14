import pygame

class movement():
    def __init__(self,screen,playerrect):
        self.screen = screen
        self.image = pygame.Surface((10,20))
        self.rect = self.image.get_frect()
        self.boost = 20
    def update(self):  
        self.screen.blit(self.image,self.rect)

class basic_attack():
    def __init__(self,screen,playerrect):
        self.screen = screen
        self.image = pygame.Surface((8,8))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_frect(topleft = playerrect.bottomright)
        self.speed = 18
    def update(self,xdirection):
        self.rect.x += self.speed * xdirection
        self.screen.blit(self.image,self.rect)

class defense():
    def __init__(self,screen,playerrect):
        self.screen = screen
        self.image = pygame.Surface((10,20))
        self.rect = self.image.get_frect()
    def update(self):
        self.screen.blit(self.image,self.rect)