# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 18:38:48 2022

@author: Haochen Tu 

Angry Plants ScreenManager
"""
import pygame
from .basicManager import BasicManager
from .gameManager import GameManager
from .levelManager import LevelManager
from modules.vector2D import Vector2
from .screenFSM import ScreenState
from .entries import Text
from .UI.displays import HoverClickMenu
from modules.soundManager import SoundManager

SCREEN_SIZE = Vector2(450, 310)

class ScreenManager(BasicManager):
      
   def __init__(self):
      super().__init__()
      self._game = LevelManager(SCREEN_SIZE)
      self._state = ScreenState()
      self._pausedText = Text(Vector2(0,0),"Paused")
      
      size = self._pausedText.getSize()
      midPointX = SCREEN_SIZE.x // 2 - size[0] // 2
      midPointY = SCREEN_SIZE.y // 2 - size[1] // 2
      
      self._pausedText.setPosition(Vector2(midPointX, midPointY))
      
      
      self._mainMenu = HoverClickMenu("startMenu.png", fontName="default8")
      self._mainMenu.addOption("start", "Start Game",
                               SCREEN_SIZE // 2 - Vector2(0,20),
                               center="both")
      self._mainMenu.addOption("exit", "Exit Game",
                               SCREEN_SIZE // 2 + Vector2(0,50),
                               center="both")
   
      self._gameOver = HoverClickMenu("gameOver.png", fontName="default8")
      self._gameOver.addOption("restart", "Restart",
                               SCREEN_SIZE // 2 - Vector2(0,20),
                               center="both")
      self._gameOver.addOption("exit", "Exit Game",
                               SCREEN_SIZE // 2 + Vector2(0,50),
                               center="both")   
      
      self._gameWin = HoverClickMenu("winScreen.png", fontName="default8")
      self._gameWin.addOption("exit", "Exit Game",
                               SCREEN_SIZE // 2 + Vector2(0,20),
                               center="both")
      
      self.playStateMusic()
   
   def setMainMenu(self, menuType):
      if menuType == "event":
         self._mainMenu = self._eventMenu
      elif menuType == "cursor":
         self._mainMenu = self._cursorMenu      
      elif menuType == "hoverclick":
         self._mainMenu = self._hoverClickMenu
   
   def draw(self, drawSurface):
      if self._state == "game":
         self._game.draw(drawSurface)
      
         if self._state.isPaused():
            self._pausedText.draw(drawSurface)
      
      elif self._state == "mainMenu":
         self._mainMenu.draw(drawSurface)
      
      elif self._state == "gameOver":
         self._gameOver.draw(drawSurface)
         
      elif self._state == "gameWin":
         self._gameWin.draw(drawSurface)
      
   def playStateMusic(self):
       songDict = {"mainMenu": "start.mp3", 
                   "gameOver": "gameOver.mp3",
                   "gameWin": "gameWin.mp3"}
       
       SoundManager.getInstance().stopMusic()
       
       if self._state._state in songDict.keys():
           SoundManager.getInstance().playMusic(songDict[self._state._state], loop = -1)
       else:
           self._game.playStateMusic()
           
               
   def handleEvent(self, event):
      # Handle screen-changing events first
      
      if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
         self._state.manageState("pause", self)
      elif event.type == pygame.KEYDOWN and event.key == pygame.K_m:
         self._state.manageState("mainMenu", self)
         

      else:
         if self._state == "game" and not self._state.isPaused():
            self._game.handleEvent(event)
         elif self._state == "mainMenu":
            choice = self._mainMenu.handleEvent(event)

            if choice == "start":
               self._state.manageState("startGame", self)
            elif choice == "exit":
               return "exit"
         elif self._state == "gameOver":
            choice = self._gameOver.handleEvent(event)
            
            if choice == "exit":
               return "exit"
            elif choice == "restart":
                
               self._game.restart()
               self._state.manageState("startGame", self)
               
         elif self._state == "gameWin":
            choice = self._gameWin.handleEvent(event)
            
            if choice == "exit":
               return "exit"

   
   
   def update(self, seconds):      
      if self._state == "game" and not self._state.isPaused():
         SCREEN_SIZE = Vector2(450, 310)
         status = self._game.update(seconds, SCREEN_SIZE)
         
         if status == "dead":
            self._state.manageState("gameOver", self)
         elif status == "gameWin":
            self._state.manageState("gameWin", self)
         
         
      elif self._state == "mainMenu":
         self._mainMenu.update(seconds)
      
      elif self._state == "gameOver":
         self._gameOver.update(seconds)
   
   def transitionState(self, state):
      self.playStateMusic()
