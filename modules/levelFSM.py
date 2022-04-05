# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 17:09:14 2022

level FSM 
"""

class LevelState(object):
   def __init__(self, state="running"):
      self._state = state # running, startLoading, transition, winning 
   
   def manageState(self, action, levelManager):
      if action == "nextLevel" and self._state == "transition":
         self._state = "startLoading"
         levelManager.transitionState("nextLevel")
            
      elif action == "doneLoading" and self._state == "startLoading":
         self._state = "running"
      
      elif action == "restart" and self._state == "running":
         self._state = "startLoading"
         levelManager.transitionState("restart")
      
      elif action == "transition" and self._state == "running":
         self._state = "transition"    
         
      elif action == "winning" and self._state == "win":
         self._state = "winning"   
   
   def __eq__(self, other):
      return self._state == other

class LevelStateThreaded(LevelState):
   def manageState(self, action, levelManager):
      if action == "load" and self._state == "startLoading":
         self._state = "loading"
      elif action == "doneLoading" and self._state == "loading":
         self._state = "running"
      else:
         super().manageState(action, levelManager)