#Screen that displays the fretboard and buttons for each note

import pygame
import os
from button import Button
from controller import play_fret, amp_on, amp_off

class PlayScreen:

    def __init__(self):
        #Loading
        self.up_img = pygame.image.load(os.path.join('assets', 'back_up.png'))
        self.down_img = pygame.image.load(os.path.join('assets', 'back_down.png'))
        self.up_img_right = pygame.transform.flip(self.up_img, True, False)
        self.down_img_right = pygame.transform.flip(self.down_img, True, False)
        self.up_touch = pygame.image.load(os.path.join('assets', 'touch_up.png'))
        self.down_touch = pygame.image.load(os.path.join('assets', 'touch_down.png'))
        self.font = pygame.font.Font(None, 30)

        #Background
        self.background = pygame.image.load(os.path.join('assets', 'background.png'))
        self.fretboard = pygame.image.load(os.path.join('assets', 'fretboard.png'))
        self.fretboard_rect = pygame.Rect((0,0), (1,1))
        
        #Back button
        self.back_btn = Button(self.up_img, self.down_img, pygame.Rect(4, 4, self.up_img.get_width(), self.up_img.get_height()))

        #Note Buttons
        self.fretpositions = [[(32,65), (0,0),(270, 61),(385, 60),(490, 58),(600, 56),(700, 55),(790, 53),(880, 51),(960, 50),(1040, 48),(1120, 46), (1185, 45)],
                              [(32,90), (0,0),(270, 89),(385, 88),(490, 88),(600, 87),(700, 87),(790, 87),(880, 86),(960, 86),(1040, 85),(1120, 85), (1185, 85)],
                              [(32,115),(0,0),(270, 116),(385, 117),(490, 118),(600, 119),(700, 120),(790, 120),(880, 121),(960, 122),(1040, 123),(1120, 124), (1185, 125)],
                              [(32,145),(0,0),(270, 148),(385, 150),(490, 151),(600, 153),(700, 155),(790, 156),(880, 158),(960, 160),(1040, 161),(1120, 163), (1185, 165)]]
        size = (32, 32)
        self.buttons = []
        for fret in range(0,11):
            for string in range(0,4):
                if fret != 1:
                    x,y = self.fretpositions[3-string][fret] 
                    rect = pygame.Rect((x-16, y-16), size)
                    btn = Button(self.up_touch, self.down_touch, rect)
                    btn.set_callback(self.note_callback)
                    btn.set_info((fret, string))
                    self.buttons.append(btn)

        slide_size = (36,30)
        left_pos = (120, 205)
        right_pos = (164, 205)
        self.slide_left  = Button(self.up_img, self.down_img, pygame.Rect(left_pos,slide_size))
        self.slide_left.set_callback(self.slide_left_callback)
        self.slide_right = Button(self.up_img_right, self.down_img_right, pygame.Rect(right_pos,slide_size))
        self.slide_right.set_callback(self.slide_right_callback)
        self.amount_moved = 0
    
    def update(self):
        pass

    def draw(self, surface):
        surface.blit(self.background, pygame.Rect(0,0,320,240))
        surface.blit(self.fretboard, self.fretboard_rect)
        self.back_btn.draw(surface)
        for btn in self.buttons:
            btn.draw(surface)
        self.slide_left.draw(surface)
        self.slide_right.draw(surface)

    def OnMouseUp(self, pos):
        self.back_btn.OnMouseUp(pos)
        self.slide_left.OnMouseUp(pos)
        self.slide_right.OnMouseUp(pos)
        for btn in self.buttons:
            btn.OnMouseUp(pos)
            
    def OnMouseDown(self, pos):
        self.back_btn.OnMouseDown(pos)
        self.slide_left.OnMouseDown(pos)
        self.slide_right.OnMouseDown(pos)
        for btn in self.buttons:
            btn.OnMouseDown(pos)

    def setBackCallback(self, callback):
        self.back_btn.set_callback(callback)

    def note_callback(self, btn):
        print("note pressed"+str(btn.info))
        print(btn.text_string)
	    amp_on()
        play_fret(btn.info[0], btn.info[1], 1)
	    amp_off()

    def slide_left_callback(self, btn):
        print("slide left")
        if self.amount_moved >= 0:
            return
        self.amount_moved += 100
        print(self.amount_moved)
        self.fretboard_rect = self.fretboard_rect.move(100,0)
        for i in range(0,len(self.buttons)):
            self.buttons[i].rect = self.buttons[i].rect.move(100,0)

    def slide_right_callback(self, btn):
        print("slide right")
        if self.amount_moved <= -900:
            return
        self.amount_moved -= 100
        print(self.amount_moved)
        self.fretboard_rect = self.fretboard_rect.move(-100,0)
        for i in range(0,len(self.buttons)):
            self.buttons[i].rect = self.buttons[i].rect.move(-100,0)
