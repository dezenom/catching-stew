import pygame,tools,sys
from player import player

damaging = pygame.USEREVENT+1
class game():
    def __init__(self,screenw,screenh,display,level):
        self.screen = display
        self.level = level
        self.screen_w,self.screen_h = screenw,screenh
        self.scroll = (0,0)
        self.camera_entities = []
        self.level_creation()
        self.spawns()
        self.entites = self.position_info()
        # menu
        self.click = False
        self.pause = False
#   level
    def level_creation(self):
        self.group = pygame.sprite.Group()
        tools.set_listtiles(self.group,self.level,16,'t','White',"normal block")
        tools.set_listtiles(self.group,self.level,16,'r','black',"trap")
        tools.set_listtiles(self.group,self.level,16,'h','light green',"heal")
        self.phsyics_bodies = [x.rect for x in self.group if x.name == 'normal block']

    def special_blocks(self):
        for blocks in self.group.sprites():
            if blocks.name == 'trap' and blocks.rect.colliderect(self.player.rect) and self.player.immunity > 100:
                self.player.damage_timer = 40
                self.player.direction.y = -6
                self.player.speedx = 6
                self.player.immunity = 0
            if blocks.name == 'heal' and blocks.rect.colliderect(self.player.rect):
                self.player.heal_timer += 4

    def position_info(self):
        entities = []
        for sprite in self.group.sprites():
            entities.append((sprite.rect.x,sprite.rect.y))
        entities.append((self.player.rect.x,self.player.rect.y))
        return entities  
    def load_pos(self):
        index = -1
        if pygame.key.get_pressed()[pygame.K_r] or self.player.health_points.current_health<0:
            for sprite in self.group.sprites():
                index +=1
                sprite.rect.x,sprite.rect.y = self.entites[index][0],self.entites[index][1]
            self.player.rect.x,self.player.rect.y = self.entites[-1][0],self.entites[-1][1]
            self.player.direction.y = 0  
            self.player.health_points.current_health = self.player.health_points.healthmax
            self.player.damage_timer,self.player.heal_timer = 0,0             
    def getscroll(self):
        scroll = [0,0]
        scroll[0] += self.player.rect.x - scroll[0] - self.screen_w/2
        scroll[1] += self.player.rect.y - scroll[1] - self.screen_h/2
        return scroll
    def camera(self):
        self.scroll = self.getscroll()
        self.scroll[0] = self.scroll[0]//10
        self.scroll[1] = self.scroll[1]//10
        for rect in self.camera_entities:
            rect.x -= self.scroll[0]
            rect.y -= self.scroll[1]
#  player
    def spawns(self):
        self.player = player((self.screen_w/2,self.screen_h/2),self.screen)
        rects = [self.player.rect]
        self.camera_entities.extend(rects)
# events
    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_SPACE:
                    self.player.jump = True
                if event.key == pygame.K_q:
                    self.player.heal_timer +=30
                if event.key == pygame.K_ESCAPE:
                    self.pause = not self.pause
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.click = True
# sprites
    def spritecontrol(self):
        self.camera()
        self.group.draw(self.screen)
        self.player.update()
        tools.platformer_physics(self.player,self.phsyics_bodies)
        self.group.update(self.scroll)
    def run(self):
        self.event_handler()
        self.spritecontrol()
        self.load_pos()
        self.special_blocks()