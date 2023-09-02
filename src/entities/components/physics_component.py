from pygame import Vector2, Rect
from typing import TYPE_CHECKING, Sequence
import game_globals
import debug
from constants import TILE_SIZE

if TYPE_CHECKING:
    from entity import Entity

class PhysicsComponent:
    def __init__(self, owner: "Entity"):
        self._owner = owner
        self._velocity = Vector2(0, 0)   # pixels per second
        self._gravity = Vector2(0, 900)  # pixels per second

        # TODO: 타일맵 어떻게 불러와야 함???
        _ = None
        self._static_tilemap = [
                [6, _, _, _, _, _, _, _, _, _, _, _, _, _],
                [6, _, _, _, _, _, _, _, _, _, _, _, _, _],
                [6, _, 2, 2, _, _, _, _, _, _, _, _, _, _],
                [6, _, _, _, _, _, _, _, _, _, _, _, _, _],
                [6, _, _, _, 2, 2, _, _, _, _, _, _, _, _],
                [6, _, _, _, 6, 6, _, 2, 2, _, _, _, _, _],
                [6, _, _, _, _, _, _, _, _, _, 2, _, _, _],
                [6, _, _, _, _, _, _, _, _, _, 6, 2, 2, _],
                [6, _, _, _, _, _, _, _, _, _, _, _, _, _],
                [6, 2, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            ]
        self._static_tilemap = map(lambda row: map(bool, row), self._static_tilemap)
        self._tile_size = TILE_SIZE
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
        
        self_rect: "Rect | None" = self.owner.get("hitbox")
        if self_rect:
            pass

    def _get_repulse_vector(self, vel: "Vector2", target_rect: "Rect"):
        my_rect: "Rect | None" = self.owner.get("hitbox")
        if not my_rect: return Vector2(0, 0)

        rect_after_move = my_rect.move(vel)
        if not rect_after_move.colliderect(target_rect): return Vector2(0, 0)

        vec_r = Vector2(0, 0)
        # TODO
        return vec_r
        

    def _update_gravity(self):
        self.velocity += self._gravity * game_globals.delta_time

    def _get_collide_rects(self):
        rects = []
        # Static Tilemap에서 rect들을 구워낸다
        # TODO: owner 근처에 있는 rect들만 뽑아내도록 하기
        tile_size = self._tile_size
        for y, row in enumerate(self._static_tilemap):
            for x, tile_exists in enumerate(row):
                if tile_exists:
                    rects.append(Rect(x, y, tile_size, tile_size))

        for rect in rects:
            debug.rect(rect)

        return rects
