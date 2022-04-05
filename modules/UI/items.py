import pygame
import os
from ..drawable import Drawable
from .screenInfo import adjustMousePos

class AbstractUIEntry(Drawable):
   """ Basic UI Entry Class
   Sets parallax to zero and contains information about fonts"""
   
   if not pygame.font.get_init():
      pygame.font.init()
   
   _FONT_FOLDER = os.path.join("resources", "fonts")   
   _DEFAULT_FONT = "PressStart2P.ttf"
   _DEFAULT_SIZE = 16
   
   FONTS = {
      "default" : pygame.font.Font(os.path.join(_FONT_FOLDER, _DEFAULT_FONT), _DEFAULT_SIZE),
      "default8" : pygame.font.Font(os.path.join(_FONT_FOLDER, _DEFAULT_FONT), 16)
   }
   
   
   def __init__(self, position):
      super().__init__("", position)
      
   
class Text(AbstractUIEntry):
   """A plain text UI entry."""
   
   def __init__(self, position, text, font="default", color=(255,255,255)):
      super().__init__(position)
      self._color = color
      
      self._image = AbstractUIEntry.FONTS[font].render(text, False, self._color)

class HoverText(Text):
   """Text which changes color when the mouse hovers over it."""
   def __init__(self, position, text, font, color, hoverColor):
      super().__init__(position, text, font, color)

      self._image = AbstractUIEntry.FONTS[font].render(text, False, color)
      self._passive = self._image
      self._hover = AbstractUIEntry.FONTS[font].render(text, False, hoverColor)
   
   def handleEvent(self, event):      
      if event.type == pygame.MOUSEMOTION:
         position = adjustMousePos(event.pos)
         if self.getCollisionRect().collidepoint(*position):
            self._image = self._hover
         else:
            self._image = self._passive
   
   def clearHover(self):
      self._image = self._passive