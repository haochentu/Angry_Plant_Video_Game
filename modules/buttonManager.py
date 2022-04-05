# -*- coding: utf-8 -*-
"""
Created on Sun Feb  6 17:16:46 2022

@author: Haochen Tu 
"""
import pygame
from .drawable import Drawable
from .vector2D import Vector2
from .animals import Fox, Otter, Cat, Panda, Dragon

class ButtonManager(object):
   
       
       def __init__(self):

           self.otter = Otter(Vector2(8, 242))
           self.fox = Fox(Vector2(33, 240))
           self.cat = Cat(Vector2(80, 242))
           self.panda = Panda(Vector2(136, 243))
           self.dragon = Dragon(Vector2(194, 238))
       
       def draw(self, surface):
            self.otter.draw(surface)
            self.fox.draw(surface)
            self.cat.draw(surface)
            self.panda.draw(surface)
            self.dragon.draw(surface)
       
       def handleEvent(self, event, adjustedPos, money):
           
           if self.otter.getCollisionRect().collidepoint(adjustedPos) and money >= 100:
               return Otter(Vector2(adjustedPos[0] - 38//2,
                                        adjustedPos[1] - 54//2))
           
           elif self.fox.getCollisionRect().collidepoint(adjustedPos) and money >= 150:
               return Fox(Vector2(adjustedPos[0] - 45//2,
                                        adjustedPos[1] - 54//2))
           
           elif self.cat.getBCollisionRect().collidepoint(adjustedPos) and money >= 200:
               return Cat(Vector2(adjustedPos[0] - 45//2,
                                        adjustedPos[1] - 54//2))

           elif self.panda.getBCollisionRect().collidepoint(adjustedPos) and money >= 350:
               return Panda(Vector2(adjustedPos[0] - 72//2,
                                        adjustedPos[1] - 53//2))

           elif self.dragon.getCollisionRect().collidepoint(adjustedPos) and money >= 500:
               return Dragon(Vector2(adjustedPos[0] - 51//2,
                                        adjustedPos[1] - 62//2))
           return None
  