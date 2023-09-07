import game_globals
from .entity import Entity
from pygame import Vector2, Rect, Surface

class BulletInfo:
    def __init__(self):
        self.surface: "Surface" = Surface((0,0))
        self.rect: "Rect" = Rect(0,0,0,0)
        self.lifetime: "float" = 3.0


class Bullet(Entity):
    def __init__(self, bullet_info: "BulletInfo", velocity: "Vector2", isEnemy=True):
        super().__init__()
        self._info = bullet_info
        self._velocity = velocity
        self._isEnemy = isEnemy

    @property
    def hitbox(self) -> "Rect":
        return self._info.rect.move(self.position)
    
    def update(self):
        from entity_manager import EntityManager
        self.position += self._velocity * game_globals.delta_time
        for ent in EntityManager.find_colliding_entities(self):
            pass