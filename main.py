import pygame,sys
sys.path.append('src')
from src.game import game
from src.settings import *

pygame.init()
screen = pygame.display.set_mode((width,height),pygame.SCALED)
clock = pygame.time.Clock()
games = game(width,height,screen,listlevel)
while True:
    clock.tick(60)
    screen.fill("red")
    games.run()
    pygame.display.flip() 