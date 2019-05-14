#Screen that displays the main menu with three buttons

import pygame
import os
from button import Button

class MenuScreen:

    def __init__(self):
        #Loading
        self.up_img = pygame.image.load(os.path.join('assets', 'button_up.png'))
        self.down_img = pygame.image.load(os.path.join('assets', 'button_down.png'))
        self.font = pygame.font.Font(None, 30)

        #Background
        self.background = pygame.image.load(os.path.join('assets', 'menu_background.png'))
        
        #Play button
        y = 45
        self.play_button = Button(self.up_img, self.down_img, pygame.Rect(200, 45, self.up_img.get_width(), self.up_img.get_height()))
        self.play_button.set_text(self.font, "Play")

        y += self.play_button.rect.height + 16
        self.songs_button = Button(self.up_img, self.down_img, pygame.Rect(200, y, self.up_img.get_width(), self.up_img.get_height()))
        self.songs_button.set_text(self.font, "Songs")

        y += self.songs_button.rect.height + 16
        self.creds_button = Button(self.up_img, self.down_img, pygame.Rect(200, y, self.up_img.get_width(), self.up_img.get_height()))
        self.creds_button.set_text(self.font, "Credit")    
    
    def update(self):
        pass

    def draw(self, surface):
        surface.blit(self.background, pygame.Rect(0,0,320,240))
        self.play_button.draw(surface)
        self.songs_button.draw(surface)
        self.creds_button.draw(surface)

    def OnMouseUp(self, pos):
        self.play_button.OnMouseUp(pos)
        self.songs_button.OnMouseUp(pos)
        self.creds_button.OnMouseUp(pos)
            
                
    def OnMouseDown(self, pos):
        self.play_button.OnMouseDown(pos)
        self.songs_button.OnMouseDown(pos)
        self.creds_button.OnMouseDown(pos)

    def setPlayCallback(self, callback):
        self.play_button.set_callback(callback)

    def setSongsCallback(self, callback):
        self.songs_button.set_callback(callback)

    def setCredsCallback(self, callback):
        self.creds_button.set_callback(callback)
    
