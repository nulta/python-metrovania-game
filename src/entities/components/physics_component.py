from pygame import Vector2, Rect
from typing import TYPE_CHECKING, Sequence
import game_globals

if TYPE_CHECKING:
    from entity import Entity

class PhysicsComponent:
    def __init__(self, owner: "Entity"):
        self._owner = owner
        self._velocity = Vector2(0, 0)   # pixels per second
        self._gravity = Vector2(0, 900)  # pixels per second
        # TODO: 맵과 엔티티의 충돌 판정 처리?
        # TODO: 엔티티와 엔티티의 충돌 판정 처리?

    @property
    def owner(self):
        return self._owner

    @property
    def velocity(self):
        return self._velocity
    
    @velocity.setter
    def velocity(self, val: "Vector2"):
        self._velocity = val


    def update(self):
        self._update_gravity()
        self.owner.position += self.velocity * game_globals.delta_time
        self._update_collision()
    
    def _update_collision(self):
        # 지금으로선 일단 바닥과의 충돌만 처리한다
        # TODO: 충돌판별을 다른 함수로 분리, 리팩토링
        # 바닥과 충돌하는가?        
        if self.owner.position.y > 500:
            self.owner.position.y = 500
            self.velocity.y = 0

    def _update_gravity(self):
        self.velocity += self._gravity * game_globals.delta_time