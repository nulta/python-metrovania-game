import game_globals
from .entity import Entity
from .components.physics_component import PhysicsComponent
from pygame import Vector2, Rect, Surface

class BulletInfo:
    def __init__(self):
        self.surface: "Surface" = Surface((0,0))
        self.rect: "Rect" = Rect(0,0,0,0)
        self.lifetime: "float" = 3.0
        self.damage: "int" = 1


class Bullet(Entity):
    def __init__(self, bullet_info: "BulletInfo", velocity: "Vector2", isEnemy=True):
        super().__init__()

        self.physics = PhysicsComponent(self)
        self.physics.no_clip = True
        self.physics.no_gravity = True
        self.physics.velocity = velocity

        self._info = bullet_info
        self._is_enemy_bullet = isEnemy
        self._remaining_time = bullet_info.lifetime


    @property
    def hitbox(self) -> "Rect":
        return self._info.rect.move(self.position)
    
    def update(self):
        from entity_manager import EntityManager
        
        hit_wall = self.physics.does_point_collide(Vector2(self.hitbox.center))
        self._remaining_time -= game_globals.delta_time
        if self._remaining_time <= 0 or hit_wall:
            return self.remove()

        for ent in EntityManager.find_colliding_entities(self):
            if self._is_enemy_bullet:
                if not ent.is_player: continue
            else:
                if not ent.is_enemy: continue
            ent.call("take_damage", self._info.damage)
            return self.remove()

    def surface(self):
        return self._info.surface