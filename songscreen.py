import pygame
import os
from button import Button
from models import play_song

class SongScreen:

    def __init__(self):
        #Loading
        self.up_img = pygame.image.load(os.path.join('assets', 'back_up.png'))
        self.down_img = pygame.image.load(os.path.join('assets', 'back_down.png'))
        self.btn_up_img = pygame.image.load(os.path.join('assets', 'button_up.png'))
        self.btn_down_img = pygame.image.load(os.path.join('assets', 'button_down.png'))
        self.btn_up_img = pygame.transform.scale(self.btn_up_img, (220, 40))
        self.btn_down_img = pygame.transform.scale(self.btn_down_img, (220, 40))

        self.font = pygame.font.Font(None, 30)

        #Background
        self.background = pygame.image.load(os.path.join('assets', 'background.png'))
        
        #Back button
        self.back_btn = Button(self.up_img, self.down_img, pygame.Rect(4, 4, self.up_img.get_width(), self.up_img.get_height()))

        self.smoke_btn = Button(self.btn_up_img, self.btn_down_img, pygame.Rect((50, 50), (220, 40)))
        self.smoke_btn.set_text(self.font, "Pachelbel's Canon")
        self.smoke_btn.set_callback(self.smoke_callback)
        self.seven_btn = Button(self.btn_up_img, self.btn_down_img, pygame.Rect((50,110), (220,40)))
        self.seven_btn.set_text(self.font, "Happy Birthday")
        self.seven_btn.set_callback(self.seven_callback)
        self.scale_btn = Button(self.btn_up_img, self.btn_down_img, pygame.Rect((50,170), (220,40)))
        self.scale_btn.set_text(self.font, "Test")    
        self.scale_btn.set_callback(self.scale_callback)

        self.title = self.font.render("Songs", True, (255,255,255))
    
    def update(self):
        pass

    def draw(self, surface):
        surface.blit(self.background, pygame.Rect(0,0,320,240))
        self.back_btn.draw(surface)
        self.smoke_btn.draw(surface)
        self.seven_btn.draw(surface)
        self.scale_btn.draw(surface)
        title_rect = self.title.get_rect()
        title_rect.center = (160, title_rect.height/2+10)
        surface.blit(self.title, title_rect)

    def OnMouseUp(self, pos):
        self.back_btn.OnMouseUp(pos)
        self.smoke_btn.OnMouseUp(pos)
        self.seven_btn.OnMouseUp(pos)
        self.scale_btn.OnMouseUp(pos)
                
    def OnMouseDown(self, pos):
        self.back_btn.OnMouseDown(pos)
        self.smoke_btn.OnMouseDown(pos)
        self.seven_btn.OnMouseDown(pos)
        self.scale_btn.OnMouseDown(pos)

    def setBackCallback(self, callback):
        self.back_btn.set_callback(callback)   

    def smoke_callback(self, btn):
        print("smoke")
        play_song(0)

    def seven_callback(self, btn):
        print("seven")
        play_song(1)

    def scale_callback(self, btn):
        print("scale") 
        play_song(2)
