# -*- coding: utf-8 -*-
"""
Created on Sat Jan 29 12:32:02 2022

@author: Haochen Tu 
"""

import pygame
from .animated import Animated

class Sunflower(Animated):
   def __init__(self, position):
      super().__init__("sunflowers.png", position, offset = None)
      self._nFrames = 8
      self._framesPerSecond = 4
