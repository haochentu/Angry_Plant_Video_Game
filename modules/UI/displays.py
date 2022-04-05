
from ..drawable import Drawable
from ..vector2D import Vector2
from .items import *
from .screenInfo import adjustMousePos
import pygame, os

class AbstractMenu(Drawable):
   """Abstract class for basic menus."""
   def __init__(self, background,
                fontName="default", color=(255,255,255)):
      super().__init__(background, (0,0))
         
      self._options = {}
      
      self._color = color      
      self._font = fontName
      self._text = []
   
   def addOption(self, key, text, position, center=None):
      self._options[key] = Text(position, text, self._font, self._color)
      
      if center != None:

         x = position[0]
         y = position[1]
         
         size = self._options[key].getSize()
         
         if center in ["horizontal", "both"]:
            x -= size[0] // 2
         
         if center in ["veritcal", "both"]:
            y -= size[1] // 2
         
         position = Vector2(x, y)
      
         self._options[key].setPosition(position)
         
   def addText(self, text, position, center=None):
         self._text.append(Text(position, text, self._font, self._color))
         
         if center != None:

            x = position[0]
            y = position[1]
            
            size = self._text[-1].getSize()
            
            if center in ["horizontal", "both"]:
               x -= size[0] // 2
            
            if center in ["veritcal", "both"]:
               y -= size[1] // 2
            
            position = Vector2(x, y)
         
            self._text[-1].setPosition(position)
   
   def draw(self, surface):
      super().draw(surface)
      
      for item in self._options.values():
         item.draw(surface)
        
   
   def update(self, ticks):
      pass
      
   def removeOption(self, key):
       self._options.pop(key)

class ClickMenu(AbstractMenu):
   """Menu which uses clicking/mouse events for selection."""
   def __init__(self, background, 
                fontName="default", color=(255,255,255)):
      super().__init__(background, fontName, color)
   
   def handleEvent(self, event):
      if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
         position = adjustMousePos(event.pos)
         
         collider = self._findCollision(position)
         
         if collider:
            return collider
   
   def _findCollision(self, position):      
      for key in self._options.keys():
         if self._options[key].getCollisionRect().collidepoint(*position):
      
            return key

class HoverClickMenu(ClickMenu):
   """Menu which uses clicking/mouse events for selection.
   Uses hover text instead of normal text."""
   
   def __init__(self, background, 
                fontName="default", color=(0,0,0),
                hoverColor=(255,0,0)):
      super().__init__(background, fontName, color)
      
      self._hoverColor = hoverColor
   
   
   def handleEvent(self, event):      
      for item in self._options.values():
         item.handleEvent(event)
      
      selection = super().handleEvent(event)
      
      if selection != None:
         self.clearHovers()
      
      return selection

   
   def addOption(self, key, text, position, center=None):
      super().addOption(key, text, position, center)
      
      t = self._options[key]
      
      self._options[key] = HoverText(t.getPosition(), text, self._font, self._color, self._hoverColor)
      
   
   def clearHovers(self):
      
      for item in self._options.values():
         item.clearHover()
         
            
class EventMenu(AbstractMenu):
   """Menu which uses event lambda functions for selection."""
   
   def __init__(self, background, fontName="default", color=(255,255,255)):
      super().__init__(background, fontName, color)
      
      self._eventMap = {}
   
   def addOption(self, key, text, position, eventLambda, center=None):
      super().addOption(key, text, position, center)
      
      self._eventMap[key] = eventLambda
   
   def draw(self, surface):      
      super().draw(surface) 
   
   def handleEvent(self, event):      
      for key in self._eventMap.keys():
         function = self._eventMap[key]
         if function(event):
            return key
         

         
   


        
   