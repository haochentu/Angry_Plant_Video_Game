# -*- coding: utf-8 -*-
"""
Created on Sat Jan 29 14:39:16 2022

@author: Haochen Tu

Collection of animals 
"""
import pygame

from .drawable import Drawable
from .vector2D import Vector2
from .animated import Animated
from .drawable import Drawable
import os
from .frameManager import FrameManager

class AbstractAnimal(Animated):
   def __init__(self, imageName, position, price, offset):
       super().__init__(imageName, position, (0,0))
       self._animate = False
       self._canMakeBullet = False 
       self._coolDown = 0 
       
       self._price = price
       
   def getPrice(self):
        return self._price

       # create bullets
   def update(self, seconds):
       
       if self._coolDown > 0:
           self._coolDown -= seconds
           if self._frame != 0:
               super().update(seconds)
               
       else:
           super().update(seconds)
           if self._frame == self._firingFrame and self._frame != self._previousFrame:
               self._canMakeBullet = True
       
       self._previousFrame = self._frame
       
   def snap(self):
       self._position[1] -= 16
       self._position[1] /= 43
       self._position[1] = round (self._position[1])
       self._position[1] *= 43
       self._position[1] += 16
       
        
class Fox(AbstractAnimal):
    def __init__(self, position):
       super().__init__("fox.png", position, 150, (0,0))
       self._nFrames = 2
       self._framesPerSecond = 1.5
       self._previousFrame = 0 
       self._firingFrame = 1   
       self._life = 60
              
       self._skull = Drawable ("skull.png", self.getSkullPosition())
       
    def draw(self, drawSurface):
        super().draw(drawSurface)
        
        if self._life <= 20:
            self._skull.draw(drawSurface)
       
    def getSCollisionRect(self):
        rect = super().getCollisionRect()
        rect.x += 32
        rect.width -= 32
        rect.y += 10
        rect.height -= 20
        return rect
    
    def getSkullPosition(self):
        rect = super().getCollisionRect()
        x = rect.x + (rect.width/2) + 9
        y = rect.y - 11
        return Vector2(x,y)
        
class Otter(AbstractAnimal):
   def __init__(self, position):
       super().__init__("otter.png", position, 100, (0,0))
       self._nFrames = 2
       self._framesPerSecond = 1.2
       self._previousFrame = 0 
       self._firingFrame = 1
       self._life = 30
       
       self._coolDown = 0 
       
       self._skull = Drawable ("skull.png", self.getSkullPosition())
       
   def draw(self, drawSurface):
        super().draw(drawSurface)
        
        if self._life <= 20:
            self._skull.draw(drawSurface)
            
   def getSkullPosition(self):
       rect = super().getCollisionRect()
       x = rect.x + (rect.width/2)-8
       y = rect.y - 13
       return Vector2(x,y)
    
   def getSCollisionRect(self):
       rect = super().getCollisionRect()
       rect.x += 4
       rect.width -= 4
       rect.y += 10
       rect.height -= 20
       return rect
        
class Cat(AbstractAnimal):
   def __init__(self, position):
       super().__init__("cat.png", position, 200, (0,0))
       self._nFrames = 3
       self._framesPerSecond = 4
       self._previousFrame = 0 
       self._firingFrame = 1
       self._life = 50
       self._skull = Drawable ("skull.png", self.getSkullPosition())
       
   def draw(self, drawSurface):
        super().draw(drawSurface)
        
        if self._life <= 20:
            self._skull.draw(drawSurface)
            
   def getSkullPosition(self):
       rect = super().getCollisionRect()
       x = rect.x + (rect.width/2)
       y = rect.y + 2
       return Vector2(x,y)
    
   def getSCollisionRect(self):
        rect = super().getCollisionRect()
        rect.x += 30
        rect.width -= 30
        rect.y += 10
        rect.height -= 25
        return rect
    
   def getBCollisionRect(self):
        rect = super().getCollisionRect()
        rect.x += 15
        rect.width -= 20
        return rect 

class Panda(AbstractAnimal):
   def __init__(self, position):
       super().__init__("panda.png", position, 350, (0,0))
       self._nFrames = 3
       self._framesPerSecond = 1.3
       self._previousFrame = 0 
       self._firingFrame = 2
       self._life = 66
       self._skull = Drawable ("skull.png", self.getSkullPosition())
       
   def draw(self, drawSurface):
        super().draw(drawSurface)
        
        if self._life <= 20:
            self._skull.draw(drawSurface)
            
   def getSkullPosition(self):
       rect = super().getCollisionRect()
       x = rect.x + (rect.width/2)-14
       y = rect.y - 18
       return Vector2(x,y)
       
   def getSCollisionRect(self):
       rect = super().getCollisionRect()
       rect.x += 24
       rect.width -= 28
       rect.y += 15
       rect.height -= 25
       return rect
   
   def getBCollisionRect(self):
        rect = super().getCollisionRect()
        rect.x += 15
        rect.width -= 28
        return rect

       
class Dragon(AbstractAnimal):
   def __init__(self, position):
       super().__init__("dragon.png", position, 500, (0,0))
       self._nFrames = 5
       self._framesPerSecond = 3
       self._previousFrame = 0 
       self._firingFrame = 4
       self._life = 100
       self._skull = Drawable ("skull.png", self.getSkullPosition())
       
   def draw(self, drawSurface):
        super().draw(drawSurface)
        
        if self._life <= 20:
            self._skull.draw(drawSurface)
            
   def getSkullPosition(self):
       rect = super().getCollisionRect()
       x = rect.x + (rect.width/2)-10
       y = rect.y - 5
       return Vector2(x,y)
       
   def getSCollisionRect(self):
       rect = super().getCollisionRect()
       rect.x += 10
       rect.width -= 10
       rect.y += 10
       rect.height -= 50
       return rect
   
