import pygame,math
from tools import frames,render_text
from support.particles import particle_system
from support.save_load_support import save_loadsystem

save_system = save_loadsystem('.save','data')

particle1 = particle_system()

class health():
    def __init__(self):
        self.healthmax = 125
        self.current_health = 125
        self.bar_image = pygame.image.load('res/health bar.png').convert_alpha()
        self.barrect = self.bar_image.get_frect(topleft = (0,0))
        self.potion_ref =  pygame.transform.scale_by(pygame.image.load('res/potion.png').convert_alpha(),2)
        self.potion_rect = self.potion_ref.get_rect(topleft = (self.barrect.w+10,10))
        self.rect = pygame.FRect(0,10,2,25)
    def draw(self,screen):
        if self.current_health > 0:
            for i in range(self.current_health):
                pos = i+20
                self.rect.x = pos
                pygame.draw.rect(screen,(255,46,98),self.rect)
        screen.blit(self.bar_image,self.barrect)
        screen.blit(self.potion_ref,self.potion_rect)

class player():
    def __init__(self,pos,screen):
        self.screen = screen
        self.image = pygame.Surface((12,16))
        self.rect = self.image.get_rect(topleft = pos)
        self.mask = pygame.mask.from_surface(self.image)
        # movement
        self.direction = pygame.Vector2((1,0))
        self.friction = 0.6
        self.speedx = 0
        self.speedy = -10
        self.maxspeed = 5
        self.acceleration = 0.8

        self.dash_speed = 15
        self.dash_cooldown = 0
        # gravity/jump
        self.gravity = 0.8
        self.on_ground = False
        self.jump = False
        self.jumpcount = 2
        self.jumpmax = 2
        # animation
        self.frames = {"idle":[],"run":[],"jump":[],"fall":[]}
        self.status = "idle"
        self.current_index = 0
        self.is_left = False
        self.getframes()
        # health
        self.hp=health()
        self.heal_timer = 0
        self.damage_timer = 0
        self.immunity = 0

        self.potions = 0
        self.potion_cooldown = 0
        # extra
        self.steps = 0
        self.maxsteps = 1000

    # player movement
    def keys(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT])and not self.dash_cooldown > 0 :
            self.dash_cooldown = 10
            self.dash()
        if self.jump and (self.on_ground or self.jumpcount <self.jumpmax):
            self.on_ground = False
            self.jumpcount += 1
            self.direction.y = 0
            self.jumping(5,self.speedy,40)
        self.jump = False
        if keys[pygame.K_a] and self.speedx < self.maxspeed:
            if self.on_ground and self.speedx > 4:
                particle1.add_particle([self.rect.x+20,self.rect.y+20])
            self.direction.x = -1
            self.is_left = True
            self.speedx += self.acceleration
        elif keys[pygame.K_d] and self.speedx < self.maxspeed:
            if self.on_ground and self.speedx > 4:
                particle1.add_particle([self.rect.x-15,self.rect.y+20])
            self.direction.x = 1
            self.is_left = False
            self.speedx += self.acceleration
    def applyfriction(self):
        self.speedx -= self.friction
        if self.speedx <= 0.1:
            self.speedx = 0
    def applygravity(self):
        self.direction.y += self.gravity if self.direction.y < 30 else 0 
        self.rect.y += self.direction.y 
    def jumping(self,repeat,vel,offset):
        particle1.particles = []
        self.direction.y = vel
        self.rect.y += self.direction.y
        for i in range(repeat * self.jumpcount):
            particle1.add_particle([self.rect.centerx,self.rect.y+offset])
    def dash(self):
        self.speedx = self.dash_speed
    def cooldowns_draw(self):
        self.immunity += 1 if self.immunity < 110 else 0
        self.dash_cooldown -= 0.1 if self.dash_cooldown > 0 else 0
        self.potion_cooldown -= 1 if self.potion_cooldown > 0 else 0

        
        pygame.draw.circle(self.screen,'violet',(self.hp.potion_rect.bottomright),self.potion_cooldown/4)
        pygame.draw.circle(self.screen,'cyan',(self.rect.x,self.rect.y -20),self.dash_cooldown/2)
        pygame.draw.circle(self.screen,(255,200,200),(self.rect.x + self.rect.w,self.rect.y -20),self.immunity/20)
    def movement(self):
        self.direction.y = 0 if self.speedx > 6 else self.direction.y
        if self.on_ground:
            self.jumpcount = 0
        
        
        self.steps += self.speedx
        self.cooldowns_draw()
        self.keys()
        self.applyfriction()
    #  animation
    def getframes(self):  
        self.brokenpath = 'res/player_animations/'
        for key in self.frames.keys():
            fullpath = self.brokenpath + key
            self.frames[key] = frames(fullpath)
    def animation(self):
        self.get_status()
        animation = self.frames[self.status]
        self.current_index+=1
        if self.current_index >= len(animation)*5:
            self.current_index = 0
        if self.is_left:
            self.image = pygame.transform.flip(animation[self.current_index//5],True,False)
        else:
            self.image = animation[self.current_index//5]
    def get_status(self):
        if self.direction.y <0:
            self.status = 'jump'
        elif self.direction.y>1:
            self.status = 'fall'
        else:
            if self.speedx <= 0.2:
                self.status = 'idle'
            else:
                self.status = 'run'
    # health 
    def damge(self):
        self.hp.current_health -= 1
    def heal(self):
        self.hp.current_health += 1
    def health_control(self):
        self.heal_timer -= 1 if self.heal_timer > 0 else 0
        self.heal_timer = 0 if self.hp.current_health == self.hp.healthmax else self.heal_timer
        self.damage_timer -= 1 if self.damage_timer > 0 else 0

        if self.heal_timer > 0 and self.hp.current_health< self.hp.healthmax:
            self.heal()
        if self.damage_timer > 0:
            self.damge()
        if pygame.key.get_pressed()[pygame.K_q]and self.potions >0 and not self.potion_cooldown> 0 and self.hp.current_health!=self.hp.healthmax:
            self.heal_timer = 20
            self.potion_cooldown = 40
            self.potions -= 1
    # variables to be saved
    def get_current_values(self):
        self.player_variables = [(self.hp.current_health,self.potions,self.potions,'healths')]
        return self.player_variables
    def save_variables(self):
        save_system.save_all_data([self.player_variables],['player_variables'])
    def load_variables(self):
        self.player_variables = save_system.load_all_data(['player_variables'],[self.get_current_values()])
        self.hp.current_health = self.player_variables[0][0]
        self.potions = self.player_variables[0][1]
        

    # update
    def update(self):
        particle1.emit(self.screen)
        self.screen.blit(self.image,self.rect)
        self.movement()
        self.animation()
        self.health_control()
        self.hp.draw(self.screen)

        render_text(self.screen,f'{self.potions}',self.hp.potion_rect.bottomleft,'res/Daydream.ttf',10)