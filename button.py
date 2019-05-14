#The Button class is used to greatly simplify the UI. Simply by providing an up image, down image and a rectangle, you can create a button. This button also supports simple callbacks for press events making for simpler, neater code. 

import pygame

class Button:
    def __init__(self, up, down, rect):
        self.rect = pygame.Rect(rect.topleft, rect.size)
        self.up = up
        self.down = down
        self.pressed = False
        self.callback = None
        self.text = None
        self.info = None
        self.text_string = ""

    def set_info(self, info):
        self.info = info

    def set_callback(self, callback):
        self.callback = callback

    def set_text(self, font, text):
        self.text_string = text
        self.text = font.render(text, True, (255,255,255))
        
    def OnMouseUp(self, pos):
        if self.pressed and self.callback is not None and self.rect.collidepoint(pos):
            self.callback(self)
        self.pressed = False
                
    def OnMouseDown(self, pos):
        self.pressed = self.rect.collidepoint(pos)
        
    def getSurface(self):
        if self.pressed:
            return self.down
        return self.up

    def draw(self, surface):
        surface.blit(self.getSurface(), self.rect)
        if (self.text is not None):
            font_rect = self.text.get_rect()
            font_rect.x = self.rect.centerx - font_rect.width/2
            font_rect.y = self.rect.centery - font_rect.height/2
            surface.blit(self.text, font_rect)
