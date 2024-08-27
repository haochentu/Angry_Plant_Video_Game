# -*- coding: utf-8 -*-
"""
Created on Sun Feb  6 18:44:35 2022

@author: Haochen
"""
import pygame

from .drawable import Drawable
from .vector2D import Vector2
from .animated import Animated
import os
from .frameManager import FrameManager


class FoxWeapon(Drawable):
   def __init__(self, position, price = None):
       super().__init__("foxweapon.png", position)
       self._velocity = Vector2(49,0) 
       self.power = 2
       self.dead = False
       
   def update(self, seconds):
       self._position -= self._velocity * seconds

   def kill(self):
        self.dead = True
    
   def isDead(self):
        return self.dead
           
class OtterWeapon(Drawable):
   def __init__(self, position, power = None):
       super().__init__("pearl.png", position)
       self._velocity = Vector2(35,0) 
       self.power = 1.5
      
   def update(self, seconds):
       self._position -= self._velocity * seconds
        
class CatWeapon(Drawable):
   def __init__(self, position, power = None):
       super().__init__("catWeapon.png", position)
       self.power = 3
       self._velocity = Vector2(45,0) 
       
   def update(self, seconds):
       self._position -= self._velocity * seconds

class PandaWeapon(Drawable):
   def __init__(self, position, power = None):
       super().__init__("pandaball.png", position)
       self.power = 5
       self._velocity = Vector2(30,0) 
       
   def update(self, seconds):
       self._position -= self._velocity * seconds
       
class DragonWeapon(Drawable):
   def __init__(self, position, power = None):
       super().__init__("fireball.png", position)
       self.power = 8
       self._velocity = Vector2(42,0) 


   # need to chase flying plants 
   def update(self, seconds):
       self._position -= self._velocity * seconds
