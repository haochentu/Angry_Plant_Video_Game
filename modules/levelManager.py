# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 17:13:35 2022

Level Manager
"""
from .basicManager import BasicManager
from .soundManager import SoundManager
from .gameManager import GameManager
from .vector2D import Vector2
from .levelFSM import LevelState, LevelStateThreaded
from .UI.displays import EventMenu, HoverClickMenu
import pygame

SCREEN_SIZE = Vector2(450, 310)

class LevelManager(BasicManager):
   
   def __init__(self, screenSize):
      self._state = LevelState()
      
      self._transitionScreen = HoverClickMenu("loading.png", fontName="default8")
      self._transitionScreen.addOption("continue", "Continue to Next Level", SCREEN_SIZE//2, center = "both")
      
      
      self._currentLevel = 0
      self._maxLevel = 3
      
      self._level = [GameManager(screenSize,
                                 "jsonLevel" + str(x) + ".txt") for x in range(self._maxLevel)]
      
      self._level[self._currentLevel].load()
      
      self._levelMusic = ["level1.mp3", "level2.mp3", "level3B.mp3"]
      

      
   def restart(self):
      self._state.manageState("restart", self)
      self._level[self._currentLevel].load()
      
   def draw(self, surface):
      if self._state == "running":
          self._level[self._currentLevel].draw(surface)
      elif self._state == "transition":
          self._transitionScreen.draw(surface)
      elif self._state == "win":
          self._winScreen.draw(surface)
          
   def playStateMusic(self):
          
          SoundManager.getInstance().stopMusic()
        
          SoundManager.getInstance().playMusic(self._levelMusic[self._currentLevel], loop = -1)
   
   def handleEvent(self, event):
      if self._state == "running":
         self._level[self._currentLevel].handleEvent(event)
         
      elif self._state == "transition":
          selection = self._transitionScreen.handleEvent(event)
          
          if selection == "continue":
              self._state.manageState("nextLevel", self)
      elif self._state == "win":
          self._state.manageState("win", self)
         
   def updateMovement(self):
      self._level[self._currentLevel].updateMovement()
         
   
   def update(self, seconds, screenSize):
      if self._state == "running":
         levelStatus = self._level[self._currentLevel].update(seconds, screenSize)
         
         if levelStatus == "nextLevel":
            if self._currentLevel == self._maxLevel - 1:
               return "gameWin"
            
            self._state.manageState("transition", self)
            
         else:
            return levelStatus
          

   def transitionState(self, state):
      if state == "nextLevel":
         self._currentLevel += 1
             
         self._level[self._currentLevel].load()
         self._state.manageState("doneLoading", self)
             
      elif state == "restart":
         self._level[self._currentLevel].load()
         
         self._state.manageState("doneLoading", self)
         
      if self._state == "running":
          self.playStateMusic()
