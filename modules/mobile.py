
from .animated import Animated
from .vector2D import Vector2

class Mobile(Animated):
   def __init__(self, imageName, position):
      super().__init__(imageName, position, offset = None)
      
   def update(self, seconds):
      
      super().update(seconds)
         
      newPosition = self.getPosition() + self._velocity * seconds
         
      self.setPosition(newPosition)
      

      