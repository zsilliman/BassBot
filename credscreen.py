import pygame
import os
from button import Button

class CredScreen:

    def __init__(self):
        #Loading
        self.up_img = pygame.image.load(os.path.join('assets', 'back_up.png'))
        self.down_img = pygame.image.load(os.path.join('assets', 'back_down.png'))
        self.font = pygame.font.Font(None, 30)

        #Background
        self.background = pygame.image.load(os.path.join('assets', 'credits_background.png'))
        
        #Back button
        self.back_btn = Button(self.up_img, self.down_img, pygame.Rect(4, 4, self.up_img.get_width(), self.up_img.get_height()))
    
    def update(self):
        pass

    def draw(self, surface):
        surface.blit(self.background, pygame.Rect(0,0,320,240))
        self.back_btn.draw(surface)

    def OnMouseUp(self, pos):
        self.back_btn.OnMouseUp(pos)
            
                
    def OnMouseDown(self, pos):
        self.back_btn.OnMouseDown(pos)

    def setBackCallback(self, callback):
        self.back_btn.set_callback(callback)    
    
