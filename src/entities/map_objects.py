from .entity import Entity
import pygame

class Ladder(Entity):
    is_static = True

    @property
    def hitbox(self):
        size = pygame.Vector2(60, 60)
        return pygame.Rect(self.position, size)
