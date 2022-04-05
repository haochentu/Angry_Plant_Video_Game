from ..vector2D import Vector2

SCREEN_SIZE = Vector2(450,310)

SCALE = 2
UPSCALED = SCREEN_SIZE * SCALE


def adjustMousePos(mousePos):
   return Vector2(*mousePos) // SCALE