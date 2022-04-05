# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 11:26:38 2022

@author: Haochen Tu

Finite State Machine for Pumpkin
"""
      
class PumpkinState(object):
   def __init__(self, state = "growing"):
      self._state = state
      
   def manageState(self, state, pumpkin):

          if state == "growing" and self._state != "growing":
               self._state = "growing" 
               pumpkin.transitionState(self._state)
              
          elif state == "walking" and self._state != "walking":
               self._state = "walking"
               pumpkin.transitionState(self._state)
              
          elif state == "dying" and self._state != "dying":
               self._state = "dying"
               pumpkin.transitionState(self._state)
               
          elif state == "died" and self._state != "died":
               self._state = "died"
           
   def getState(self):
      return self._state


