import pygame,math
from os import walk

def get_image(size,image_source,frame):
    image = pygame.Surface((size,size))
    image.blit(pygame.image.load(image_source),(frame*-size,0,size,size))
    image.set_colorkey((0,0,0))

    return image

class tile(pygame.sprite.Sprite):
    def __init__(self,pos,imagesource,group,name,frame,x,y,z,ramp_type):
        super().__init__(group)
        self.image = get_image(16,imagesource,frame)
        self.name = name
        self.level_x,self.level_y,self.level_z = x,y,z
        self.ramp_type = ramp_type
        self.rect = self.image.get_frect(topleft=pos)
        self.mask = pygame.mask.from_surface(self.image)
    def update(self,direction):
        self.rect.x -= direction[0]
        self.rect.y -= direction[1]

class buttons ():
    def __init__(self,pos,screen,scale,imagepath) :
        self.screen = screen
        image = pygame.image.load(imagepath).convert_alpha()
        self.image = pygame.transform.scale(image,scale)
        self.rect = self.image.get_frect(topleft = pos)
        self.collide = False
    def update(self,text):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.collide = True
        else:
            self.collide = False
        self.screen.blit(self.image,self.rect)
        render_text(self.screen,text,(self.rect.centerx,self.rect.centery),'res/Daydream.ttf',10)

def render_text(screen,text,pos,fonts,size):
    font = pygame.font.Font(fonts,size)
    text = font.render(text,False,(50,50,50))
    rect = text.get_rect(center = pos)
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

def collision_list(group,player):
    hit_list = []
    for rect in group:
        rect.colliderect(player)
        hit_list.append(rect)
    return hit_list

def array_tiles(group,level,size,name,imagesource,zpos,ramp_type):
    for row_index,row in enumerate(level):
        for col_index,col in enumerate(row):
            y = row_index * size
            x = col_index * size
            if col>-1:
                tiles = tile((x,y),imagesource,group,name,col,col_index,row_index,zpos,ramp_type)




def platformer_physics(player,physics_bodies,ramp_right):
    hitlist = collision_list(physics_bodies,player)
    def collision():
        player.applygravity()
        for rect in hitlist:
            if rect.colliderect(player.rect):
                if player.direction.y > 0: 
                    player.rect.bottom = rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = rect.bottom
                    player.direction.y = 0
        if player.direction.y > 1 or player.direction.y < 0:
            player.on_ground = False

        player.rect.x += player.direction.x * player.speedx
        for rect in hitlist:
            if rect.colliderect(player.rect):
                if player.direction.x < 0: 
                    player.rect.left = rect.right
                elif player.direction.x > 0:
                    player.rect.right = rect.left
    def ramp_collision():
        for ramp_info in ramp_right:
            if player.rect.colliderect(ramp_info[0]):
                rel_x = player.rect.x - ramp_info[0].x
                player.direction.y = 0
                player.on_ground = True
                
                if ramp_info[1] == "left":
                    pos_height = rel_x + ramp_info[0].width
                if ramp_info[1] == "right":
                    pos_height = ramp_info[0].h - rel_x  

                pos_height = min(pos_height,ramp_info[0].h)
                pos_height = max(pos_height,0) 
                target_y = ramp_info[0].y + ramp_info[0].h - pos_height
                if player.rect.bottom > target_y:
                    player.rect.bottom = target_y
    
    collision()
    ramp_collision()

    return player.rect