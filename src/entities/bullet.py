from pygame.math import Vector2
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
        self._pivot = Vector2(bullet_info.surface.get_size()) // 2


    @property
    def hitbox(self) -> "Rect":
        return self._info.rect.move(self.position - self.pivot)
    
    def update(self):
        super().update()
        from entity_manager import EntityManager

        # 물리 처리
        self.physics.update()
        
        # 탄 제거 체크
        hit_wall = self.physics.does_point_collide(Vector2(self.hitbox.center))
        self._remaining_time -= game_globals.delta_time
        if self._remaining_time <= 0 or hit_wall:
            print("Rect", repr(self._info.rect))
            return self.remove()

        # 닿는 물체가 있는지 확인
        for ent in EntityManager.find_colliding_entities(self):
            if self._is_enemy_bullet:
                if not ent.is_player: continue
            else:
                if not ent.is_enemy: continue
            ent.call("take_damage", self._info.damage)
            return self.remove()

    def surface(self):
        return self._info.surface