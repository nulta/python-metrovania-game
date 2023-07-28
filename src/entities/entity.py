from pygame.math import Vector2
from constants import *

class Entity():
    def __init__(self):
        self._position = Vector2(0, 0)
        self._valid = True

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value
    
    @property
    def valid(self):
        """이 개체가 유효한지 여부. 유효하지 않은 개체는 사용해서는 안 된다."""
        return self._valid


    def update(self):
        pass

    def draw(self):
        pass

    def remove(self):
        """자신을 삭제하도록 요청한다. 실제 삭제는 나중 프레임에서 이루어진다."""
        self._valid = False
