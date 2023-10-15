import pygame,sys

pygame.init()

sys.path.append('src')

from src.game import game
from src.tools import buttons
from src.settings import *

screen = pygame.display.set_mode((width,height),pygame.SCALED)
clock = pygame.time.Clock()

    

def game_loop():
    global running_game
    pause = buttons((width - 70,5),screen,1,'res/pause_button.png')
    games = game(width,height,screen,listlevel)
    running_game = True

    while running_game:
        screen.fill("grey")
        clock.tick(60)

        games.run()
        pause.update('')
        # control collision with buttons
        if pause.collide and games.click:
            pause_menu()
        if games.pause:
            pause_menu()
            games.pause = False
        games.click = False
        
        pygame.display.flip()
def pause_menu():
    global pause_running
    resume = buttons((width/2 -40,50),screen,1,'res/button.png')
    pause_running = True
    kill = False
    while pause_running:
        screen.fill((0, 255, 255), None, pygame.BLEND_RGBA_MULT)
        clock.tick(60)
        click = False
        
        resume.update('resume')
        
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                pause_running = False
                kill = True
            if events.type == pygame.KEYDOWN:
                if events.key == pygame.K_ESCAPE:
                    pause_running = False
            if events.type == pygame.MOUSEBUTTONDOWN:
                click = True


        # control collision with buttons
        if (resume.collide and click):
            pause_running = False
        pygame.display.flip() 


    if kill:
        pygame.quit()
        sys.exit()
        
game_loop()