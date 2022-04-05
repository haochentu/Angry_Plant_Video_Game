# -*- coding: utf-8 -*-
"""
Created on Sat Jan 29 11:47:13 2022

@author: Haochen Tu 

Tower Defense Video Game - Angry Plants

"""

import pygame 
import os
import random
from modules.vector2D import Vector2
from modules.frameManager import FrameManager
from modules.buttonManager import ButtonManager
from modules.sunflower import Sunflower
from modules.animals import Fox, Otter, Cat, Panda, Dragon
from modules.weapons import FoxWeapon, OtterWeapon, CatWeapon, PandaWeapon, DragonWeapon
from modules.enemy import Cactus, Mushroom, Pumpkin, Flower
from modules.gameManager import GameManager
from modules.screenManager import ScreenManager

SCREEN_SIZE = Vector2(450, 310)
SCALE = 2
UPSCALED = SCREEN_SIZE * SCALE

def main():
   
   # initialize the pygame module
   pygame.init()
   
   # load and set the logo
   pygame.display.set_caption("Angry Plants")
   
   # obtain the screen
   screen = pygame.display.set_mode(list(UPSCALED))
   
   drawSurface = pygame.Surface(list(SCREEN_SIZE))
   
   screenManager = ScreenManager()
   
   # load background
   
   gameClock = pygame.time.Clock()
   
   # define a variable to control the main loop
   RUNNING = True
   
   # main loop
   while RUNNING:
       
      screenManager.draw(drawSurface)
      
      pygame.transform.scale(drawSurface, list(UPSCALED), screen)
      
      # Flip the display to the monitor
      pygame.display.flip()
      
      # event handling, gets all event from the eventqueue
      for event in pygame.event.get():
         # only do something if the event is of type QUIT or ESCAPE is pressed
         if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            # change the value to False, to exit the main loop
            RUNNING = False   
            break 
            
         result = screenManager.handleEvent(event)
         
         if result == "exit":
            RUNNING = False
            break
    
    #------------------------------------------------------------------
                   
      gameClock.tick()
      
      seconds = gameClock.get_time() / 1000
      
      screenManager.update(seconds)

   pygame.quit()
            
if __name__ == "__main__":
   main()


