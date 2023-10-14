import pygame,math
from os import walk

class tile(pygame.sprite.Sprite):
    def __init__(self,pos,surf,group,colour,name):
        super().__init__(group)
        self.image = surf
        self.image.fill(colour)
        self.name = name
        self.rect = self.image.get_frect(topleft=pos)
        self.mask = pygame.mask.from_surface(self.image)
    def update(self,direction):
        self.rect.x -= direction[0]
        self.rect.y -= direction[1]

class buttons ():
    def __init__(self,pos,screen,scale,imagepath) :
        self.screen = screen
        image = pygame.image.load(imagepath).convert_alpha()
        self.image = pygame.transform.scale_by(image,scale)
        self.rect = self.image.get_frect(center = pos)
        self.collide = False
    def update(self,rendertext,text):
        s = 0
        s+=1
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.collide = True
        else:
            self.collide = False
        self.rect.y += math.sin(s)
        self.screen.blit(self.image,self.rect)
        rendertext(self.screen,text,(self.rect.centerx,self.rect.centery))

def render_text(screen,text,pos,fonts,size):
    font = pygame.font.Font(fonts,size)
    text = font.render(text,False,(0,0,0))
    rect = text.get_rect(topleft = pos)
    screen.blit(text,rect)
    
def frames(path):
    surface_list=[]
    for i,ii,filename in walk(path):
        for file in filename:
            file = path + '/' + file
            image= pygame.transform.scale_by(pygame.image.load(file).convert_alpha(),0.5)
            surface_list.append(image)
    return surface_list 

def check_maskcollision(group,playergroup,dokill):
        player = playergroup.sprite
        for sprite in group.sprites():
            if player.rect.colliderect(sprite):
                return pygame.sprite.spritecollide(player,group,dokill,pygame.sprite.collide_mask)

def rect_collision(group,playergroup):
    player = playergroup.sprite
    for sprite in group.sprites():
        if player.rect.colliderect(sprite):
            return pygame.sprite.spritecollide(player,group,False)

def collision_list(group,playergroup):
    player = playergroup.sprite
    hit_list = []
    for sprite in group.sprites():
        if sprite.rect.colliderect(player):
            hit_list.append(sprite)
    return hit_list

def set_pytmx_tiles(name,group,level):
        for x,y,surf in level.get_layer_by_name(name).tiles():
            pos = x*16,y*16
            surf = surf
            tiles = tile(pos,surf,group) 

def set_listtiles(group,level,size,tilesign,colour,name):
    for col_index,col in enumerate(level):
        for row_index,row in enumerate(col):
            y = col_index * size
            x = row_index * size
            if row == tilesign:
                tiles = tile((x,y),pygame.Surface((size,size)),group,colour,name)

def platformer_physics(player,physics_bodies):
    def xcollision():
        player.rect.x += player.direction.x * player.speedx
        for rect in physics_bodies:
            if rect.colliderect(player.rect):
                if player.direction.x < 0: 
                    player.rect.left = rect.right
                elif player.direction.x > 0:
                    player.rect.right = rect.left          
    def ycollision():
        player.applygravity()
        for rect in physics_bodies:
            if rect.colliderect(player.rect):
                if player.direction.y > 0: 
                    player.rect.bottom = rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = rect.bottom
                    player.direction.y = 0
    ycollision()
    xcollision()