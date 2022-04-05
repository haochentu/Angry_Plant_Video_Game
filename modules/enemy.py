# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 00:19:06 2022

@author: Haochen Tu 

Collection of enemies 
"""
import pygame
import random 
import math
from .vector2D import Vector2
import os
from .mobile import Mobile
from .pumpkinFSM import PumpkinState
from .flowerFSM import FlowerState
from .frameManager import FrameManager


class AbstractEnemy(Mobile):
   def __init__(self, imageName, position):
       super().__init__(imageName, position)
           
   def update(self, seconds):
       super().update(seconds)
       
   def froze(self):
       self._velocity = Vector2(0,0)
       
class Cactus(AbstractEnemy):
    def __init__(self, position):
       super().__init__("cactus.png", position)
       self._nFrames = 8
       self._framesPerSecond = 2

       self._lifeValue = 14
       self._velocity = Vector2(12,0) 
       self._reward = 100
       self._attack = 5.5
       
    def recover(self):
        self._velocity = Vector2(12,0)

    def getSCollisionRect(self):
        rect = super().getCollisionRect()
        rect.width -= 20
        rect.y += 10
        rect.height -= 20
        return rect
        
class Dandelion(AbstractEnemy):
    def __init__(self, position):
       super().__init__("dandelion.png", position)
       self._nFrames = 10
       self._framesPerSecond = 3

       self._lifeValue = 135
       self._velocity = Vector2(10,0) 
       self._reward = 300
       self._attack = 0
       
    def update(self, seconds, x):
          
       super().update(seconds)
       
       if seconds <= 0.002:
           lowvalue = 15
           uppervalue = 30
       elif 0.002 < seconds <= 0.004:
           lowvalue = 8
           uppervalue = 10
       elif 0.004 < seconds <= 0.006:
           lowvalue = 0.8
           uppervalue = 0.9
       else:
           lowvalue = 0.9
           uppervalue = 1
           seconds = random.uniform(0.04, 0.06)
             
       newPosition = self.getPosition() + Vector2(5, math.sin(int(x/640)) * random.uniform(lowvalue, uppervalue) * math.pi)*seconds

       self.setPosition(newPosition)        

class Mushroom(AbstractEnemy):
    def __init__(self, position):
       super().__init__("mushroom.png", position)
       self._nFrames = 3
       self._framesPerSecond = 1

       self._lifeValue = 40
       self._velocity = Vector2(18,0) 
       self._reward = 180
       self._attack = 5
    
    def recover(self):
        self._velocity = Vector2(18,0)

    def getSCollisionRect(self):
        rect = super().getCollisionRect()
        rect.width -= 15
        return rect

class Pumpkin(AbstractEnemy):
    def __init__(self, position):
        super().__init__("pumpkin.png", position)
        
        self._nFrames = 6
        self._framesPerSecond = 3
        
        self._lifeValue = 50
        self._velocity = Vector2(0,0) 
        self._reward = 150
        self._attack = 7
        
        self._growTimer = 0 
        self._deathTimer = 0
          
        self._nFramesList = {
             "growing" : 6,
             "walking" : 8, 
             "dying":3
          }
          
        self._rowList = {
             "growing" : 0,
             "walking" : 1,
             "dying" : 2
          }
          
        self._framesPerSecondList = {
             "growing" : 3,
             "walking" : 3, 
             "dying" : 3
          }
          
        self._state = PumpkinState()
    
    def update(self, seconds):
        
        if self._state.getState() == "growing":
            self._growTimer += seconds
            if self._growTimer > 2:
                self._state.manageState("walking", self)
                
        elif self._state.getState() == "walking":
            if self._lifeValue < 0:
                self._state.manageState("dying", self)
            
        elif self._state.getState() == "dying":
            self._deathTimer += seconds
            if self._deathTimer > 1:
                self._state.manageState("died", self)
        
        super().update(seconds)
            
    def recover(self):
        if self._state.getState() == "walking":
            self._velocity = Vector2(15,0)

    def getSCollisionRect(self):
        rect = super().getCollisionRect()
        rect.width -= 15
        return rect
        
    def transitionState(self, state):
        self._nFrames = self._nFramesList[state]
        self._frame = 0
        self._row = self._rowList[state]
        self._framesPerSecond = self._framesPerSecondList[state]
        self._animationTimer = 0
        self.setImage(FrameManager.getInstance().getFrame(self._imageName, (self._frame, self._row)))

        if state == "growing":
            self._velocity = Vector2(0,0)
   
        elif state == "walking":
            self._velocity = Vector2(15,0)
         
        elif state == "dying":
            self._velocity = Vector2(0,0)


class Flower(AbstractEnemy):
    def __init__(self, position):
        super().__init__("flower.png", position)
        
        self._nFrames = 4
        self._framesPerSecond = 2
        
        self._lifeValue = 20
        self._velocity = Vector2(0,0) 
        self._reward = 150
        self._attack = 3
        
        self._growTimer = 0 
        self._deathTimer = 0
          
        self._nFramesList = {
             "growing" : 4,
             "walking" : 3, 
          }
          
        self._rowList = {
             "growing" : 0,
             "walking" : 1,
          }
          
        self._framesPerSecondList = {
             "growing" : 2,
             "walking" : 3, 
          }
          
        self._state = FlowerState()
    
    def update(self, seconds):
        
        if self._state.getState() == "growing":
            self._growTimer += seconds
            if self._growTimer > 2:
                self._state.manageState("walking", self)
                
        elif self._state.getState() == "walking":
            if self._lifeValue < 0:
                self._state.manageState("died", self)
         
        super().update(seconds)
            
    def recover(self):
        if self._state.getState() == "walking":
            self._velocity = Vector2(20,0)
        
    def transitionState(self, state):
        self._nFrames = self._nFramesList[state]
        self._frame = 0
        self._row = self._rowList[state]
        self._framesPerSecond = self._framesPerSecondList[state]
        self._animationTimer = 0
        self.setImage(FrameManager.getInstance().getFrame(self._imageName, (self._frame, self._row)))

        if state == "growing":
            self._velocity = Vector2(0,0)
   
        elif state == "walking":
            self._velocity = Vector2(20,0)

    def getSCollisionRect(self):
        rect = super().getCollisionRect()
        rect.width -= 15
        return rect

