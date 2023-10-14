import pygame,math
from tools import frames
from particles.basic import particle_system

particle1 = particle_system()

class health():
    def __init__(self):
        self.healthmax = 125
        self.current_health = 125
        self.bar_image = pygame.image.load('res/health bar.png').convert_alpha()
        self.barrect = self.bar_image.get_frect(topleft = (0,0))
        self.rect = pygame.FRect(0,10,2,25)
    def draw(self,screen):
        if self.current_health > 0:
            for i in range(self.current_health):
                pos = i+20
                self.rect.x = pos
                pygame.draw.rect(screen,(255,46,98),self.rect)
        screen.blit(self.bar_image,self.barrect)


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

        self.dash_cooldown = 0
        # gravity/jump
        self.gravity = 0.8
        self.on_ground = False
        self.timer = 5
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
        self.health_points=health()
        self.heal_timer = 0
        self.damage_timer = 0
        self.immunity = 0

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
            self.timer = 0
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
        self.on_ground = False if self.timer <= 0 else True
        self.direction.y += self.gravity if self.direction.y < 30 else 0 
        self.rect.y += self.direction.y 
    def jumping(self,repeat,vel,offset):
        particle1.particles = []
        self.direction.y = vel
        self.rect.y += self.direction.y
        for i in range(repeat * self.jumpcount):
            particle1.add_particle([self.rect.centerx,self.rect.y+offset])
    def dash(self):
        self.speedx = 13
        self.rect.x += self.speedx * self.direction.x
    def cooldowns_draw(self):
        self.immunity += 1 if self.immunity < 110 else 0
        self.dash_cooldown -= 0.1 if self.dash_cooldown > 0 else 0
        pygame.draw.circle(self.screen,'cyan',(self.rect.x,self.rect.y -20),self.dash_cooldown/2)
        pygame.draw.circle(self.screen,(255,200,200),(self.rect.x + self.rect.w,self.rect.y -20),self.immunity/20)
    def movement(self):
        self.gravity = 0 if self.speedx > 6 else 0.8
        if self.on_ground:
            self.jumpcount = 0
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
        self.health_points.current_health -= 1
    def heal(self):
        self.health_points.current_health += 1
    def health_control(self):
        self.heal_timer -= 1 if self.heal_timer > 0 else 0
        self.damage_timer -= 1 if self.damage_timer > 0 else 0
        if self.heal_timer > 0 and self.health_points.current_health< self.health_points.healthmax:
            self.heal()
        if self.damage_timer > 0:
            self.damge()
    # update
    def update(self):
        particle1.emit(self.screen)
        self.screen.blit(self.image,self.rect)
        self.movement()
        self.animation()
        self.health_control()
        self.health_points.draw(self.screen)