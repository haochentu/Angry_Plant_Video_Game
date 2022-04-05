# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 13:29:33 2022

Angry Plants BasicManager
"""

class BasicManager(object):

   def draw(self, drawSurface):
      raise NotImplementedError("Draw not implemented.")
   
   def update(self, ticks):
      raise NotImplementedError("Update not implemented.")
   
   def handleEvent(self, event):
      raise NotImplementedError("Handle event not implemented.")