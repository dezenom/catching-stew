import pygame,sys

pygame.init()

sys.path.append('src')

from src.game import game
from src.tools import buttons
from src.settings import *

screen = pygame.display.set_mode((width,height),pygame.SCALED)
clock = pygame.time.Clock()

def main_menu():
    play = buttons((20,50),screen,(100,50),'res/button.png')
    options = buttons((20,50+play.rect.h + 30),screen,(150,50),'res/button.png')
    shop = buttons((20,50+play.rect.h*2 + 60),screen,(180,50),'res/button.png')
    exit = buttons((20,50+play.rect.h*3 + 90),screen,(220,50),'res/button.png')
    while True:
        screen.fill((0, 255, 255))
        clock.tick(60)
        click = False
        
        play.update('play'.upper())
        options.update('options'.upper())
        shop.update('shop'.upper())
        exit.update('exit'.upper())
        
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  
            if events.type == pygame.MOUSEBUTTONDOWN:
                click = True


        # control collision with buttons
        if play.collide and click:
            game_loop()
        if options.collide and click:
            options_menu()
        if shop.collide and click:
            shop_menu()
        if exit.collide and click:
            games.save
            pygame.quit()
            sys.exit()  
        pygame.display.flip()

def options_menu():
    video = buttons((20,50),screen,(80,50),'res/button.png')
    audio = buttons((20,50+video.rect.h + 50),screen,(80,50),'res/button.png')
    save = buttons((20,50+video.rect.h*2 + 100),screen,(80,50),'res/button.png')
    options_running = True
    while options_running:
        screen.fill('grey')
        clock.tick(60)
        click = False
        
        video.update('video'.upper())
        audio.update('audio'.upper())
        save.update('save'.upper())
        
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  
            if events.type == pygame.MOUSEBUTTONDOWN:
                click = True


        # control collision with buttons
        if video.collide and click:
            pass
        if audio.collide and click:
            pass
        if save.collide and click:
            pass
         
        pygame.display.flip()
def shop_menu():
    pass

def game_loop():
    global running_game, games
    pause = buttons((width - 70,5),screen,(50,50),'res/pause_button.png')
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
    global running_game
    resume = buttons((width/2 -40,70),screen,(100,50),'res/button.png')
    options = buttons((width/2 -145,70+resume.rect.h + 30),screen,(150,50),'res/button.png')
    exit = buttons((width/2 -40,70+resume.rect.h*2 + 60),screen,(220,50),'res/button.png')
    pause_running = True
    while pause_running:
        screen.fill((0, 255, 255), None, pygame.BLEND_RGBA_MULT)
        clock.tick(60)
        click = False
        
        resume.update('resume'.upper())
        options.update('options'.upper())
        exit.update('exit to mainmenu'.upper())
        
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if events.type == pygame.KEYDOWN:
                if events.key == pygame.K_ESCAPE:
                    pause_running = False
            if events.type == pygame.MOUSEBUTTONDOWN:
                click = True


        # control collision with buttons
        if resume.collide and click:
            pause_running = False
        if options.collide and click:
            options_menu()
        if exit.collide and click:
            pause_running = False
            running_game = False
            games.save()
        pygame.display.flip()

main_menu()