import pygame as pg
from tools import render_text

class NPC(pg.sprite.Sprite):
    def __init__(self,group,pos,surface,text_list,screen,player_rect):
        super().__init__(group)
        self.screen = screen
        self.image = surface
        self.image.fill((0,0,0))
        self.rect = self.image.get_rect(topleft = pos)
        self.text_list = text_list
        self.chat = dialogue(player_rect,[self.rect,
                                          self.text_list])
    def update(self,pressed):
        self.next = pressed
        self.screen.blit(self.image,self.rect)
        self.chat.draw_text(self.screen,self.next)
    
class dialogue():
    def __init__(self,player_rect,npc_info):
        self.npc = npc_info
        self.rect = player_rect
        self.text_index = 0
    def check_distance(self)->bool:
        if abs((self.rect.x + self.rect.y) - (self.npc[0].x+self.npc[0].y)) < 30:
            return True
        else:False
    
    def next_text(self,key_value):
        if self.check_distance() and key_value and self.text_index < len(self.npc[1]) -2:
            self.text_index += 1
            print("hey")
    
    def draw_text(self,screen,key_value):
        self.next_text(key_value)
        self.line_2 = self.text_index +1 if not self.text_index + 1 > len(self.npc[1])-1 else 0
        if self.check_distance():
            render_text(screen,self.npc[1][self.text_index],
                        (self.npc[0].x-self.npc[0].w-10,self.npc[0].y - self.npc[0].h-10),
                        "res/Daydream.ttf",5)
            render_text(screen,self.npc[1][self.line_2],
                        (self.npc[0].x-self.npc[0].w,self.npc[0].y - self.npc[0].h),
                        "res/Daydream.ttf",10)
