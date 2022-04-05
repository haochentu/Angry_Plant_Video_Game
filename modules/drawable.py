import pygame
from pygame import image
import os
from .vector2D import Vector2
from .frameManager import FrameManager

class Drawable(object):
   """Anything that can be drawn in the game inherits from this class."""

   def __init__(self, imageName, position, offset = None):
      self._imageName = imageName
      
      fm = FrameManager.getInstance()
      
      if self._imageName != "":
          self._image = fm.getFrame(self._imageName, offset)

      self._position = Vector2(*position)
      
      
   def getPosition(self):
      return self._position

   def setPosition(self, newPosition):
      self._position = newPosition
      
   def getSize(self):
      return self._image.get_size()
   
   def setImage(self, surface):
      self._image = surface
   
   def getWidth(self):
       return self._image.get_width()

   def getHeight(self):
       return self._image.get_height()

   def getCollisionRect(self):
      newRect =  self._position + self._image.get_rect()
      return newRect
   
   def draw(self, surface):
      surface.blit(self._image, (self._position[0], self._position[1]))
      

     