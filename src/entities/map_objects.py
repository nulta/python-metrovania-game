from .entity import Entity
import pygame

class StaticEntity(Entity):
    is_static = True

    @property
    def hitbox(self):
        size = pygame.Vector2(60, 60)
        return pygame.Rect(self.position, size)

class Ladder(StaticEntity):
    pass

class Stair(StaticEntity):
    def __init__(self, to_left: bool):
        super().__init__()
        self._to_left = to_left

class Spike(StaticEntity):
    pass

class BoostTile(StaticEntity):
    def __init__(self, boost: float=1):
        super().__init__()
        self._boost = boost
