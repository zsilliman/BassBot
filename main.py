import sys
 
import pygame
from pygame.locals import *
from menu import MenuScreen
import os
from playscreen import PlayScreen
from songscreen import SongScreen
from credscreen import CredScreen
from controller import clean, is_running

os.putenv('SDL_VIDEODRIVER','fbcon')
os.putenv('SDL_FBDEV','/dev/fb1')
os.putenv('SDL_MOUSEDRV', 'TSLIB') # Track mouse clicks on piTFT
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')
 
pygame.init()
 
fps = 30
fpsClock = pygame.time.Clock()
 
size = width, height = 320, 240
screen = pygame.display.set_mode(size)
pygame.mouse.set_visible(False)

#Create Screens
menu_screen = MenuScreen()
play_screen = PlayScreen()
song_screen = SongScreen()
cred_screen = CredScreen()
screen_lst = [menu_screen, play_screen, song_screen, cred_screen]
current_screen = 0

#Screen callbacks
def play_callback(btn):
  global current_screen
  print("play pressed")
  current_screen = 1

def songs_callback(btn):
  global current_screen
  print("songs pressed")
  current_screen = 2

def cred_callback(btn):
  global current_screen
  print("creds pressed")
  current_screen = 3

screen_lst[0].setPlayCallback(play_callback)
screen_lst[0].setSongsCallback(songs_callback)
screen_lst[0].setCredsCallback(cred_callback)

def back_callback(btn):
  global current_screen
  print("back")
  current_screen = 0
  
screen_lst[1].setBackCallback(back_callback)
screen_lst[2].setBackCallback(back_callback)
screen_lst[3].setBackCallback(back_callback)
 
# Game loop.
try:
  while is_running():
    screen.fill((0, 0, 0))
  
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
      elif event.type == pygame.MOUSEBUTTONUP:
        pos = pygame.mouse.get_pos()
        screen_lst[current_screen].OnMouseUp(pos)
      elif event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        screen_lst[current_screen].OnMouseDown(pos)
      
    # Update.
    screen_lst[current_screen].update()
  
    # Draw.
    screen_lst[current_screen].draw(screen)

    pygame.display.flip()
    fpsClock.tick(fps)

except KeyboardInterrupt:
  clean()

pygame.quit()
clean()
