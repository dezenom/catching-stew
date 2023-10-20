import pygame,tools,sys
from player import player
from save_load_support import save_loadsystem

save_system = save_loadsystem('.save','data')
class game():
    def __init__(self,screenw,screenh,display,level):
        self.screen = display
        self.level = save_system.load_all_data(["level_data"],[level])
        self.screen_w,self.screen_h = screenw,screenh
        self.scroll = (0,0)
        self.camera_entities = []
        # level/world
        self.level_creation()
        self.spawns()
        # load
        self.entites_pos = save_system.load_all_data(['entity_pos'],[self.position_info()])
        self.load_pos()
        self.player.load_variables()
        # menu
        self.click = False
        self.pause = False
#   level
    def level_creation(self):
        self.group = pygame.sprite.Group()
        size = 16
        tools.set_listtiles(self.group,self.level[0],16,"normal block","res/world art/tileset.png",0)
        tools.set_listtiles(self.group,self.level[1],16,"bg","res/world art/tileset.png",1)
        self.phsyics_bodies = [x.rect for x in self.group if x.name == 'normal block']
    def special_blocks(self):
        for block in self.group.sprites():
            if block.name == 'trap' and block.rect.colliderect(self.player.rect) and self.player.immunity > 100:
                self.player.damage_timer = 40
                self.player.direction.y = -6
                self.player.speedx = 6
                self.player.immunity = 0
            if block.name == 'heal' and block.rect.colliderect(self.player.rect):
                self.player.heal_timer += 4
            if block.name == 'potion' and block.rect.colliderect(self.player.rect):
                self.level[block.level_z,block.level_y,block.level_x] = -1
                self.group.remove(block)
                self.player.potions += 1


# save system,
    def position_info(self):
        entities = []
        for sprite in self.group.sprites():
            entities.append((sprite.rect.x,sprite.rect.y))
        entities.append((self.player.rect.x,self.player.rect.y))
        return entities 
    def load_pos(self):
        index = -1
        for sprite in self.group.sprites():
            index +=1
            sprite.rect.x,sprite.rect.y= self.entites_pos[index][0],self.entites_pos[index][1]
        self.player.rect.x,self.player.rect.y = self.entites_pos[-1][0],self.entites_pos[-1][1]
        self.player.direction.y = 0  
        self.player.damage_timer,self.player.heal_timer = 0,0
    def save(self):
        self.entites_pos = self.position_info()
        save_system.save_all_data([self.entites_pos,self.level],['entity_pos','level_data'])
        
        self.player.player_variables = self.player.get_current_values()
        self.player.save_variables()
    def checkpoints(self):
        if self.player.steps > self.player.maxsteps and self.player.on_ground and self.player.speedx == 0:
            self.save()
            self.player.steps = 0
    def respawn(self):
        if self.player.hp.current_health <= 0 or self.player.rect.y > self.screen_h+20:
            self.load_pos()
            self.player.hp.current_health = self.player.hp.healthmax
 
#camera  
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
        self.player = player((100,100),self.screen)
        rects = [self.player.rect]
        self.camera_entities.extend(rects)
# events
    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.save()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_SPACE:
                    self.player.jump = True
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
        self.checkpoints()
        self.respawn()
        self.event_handler()
        self.spritecontrol()
        self.special_blocks()