from entities.components.physics_component import PhysicsComponent
from .entity import Entity
import pygame
from pygame import Rect,Vector2
from .components.physics_component import PhysicsComponent
from constants import TILE_SIZE, PHYSICS_STAIR_HEIGHT, DEBUG_DRAW_HITBOX
import debug
from resource_loader import ResourceLoader
from .player import *

class StaticEntity(Entity):
    is_static = True

    @property
    def hitbox(self):
        size = Vector2(60, 60)
        return Rect(self.position, size)
    
    def on_physics_trigger(self, phys: "PhysicsComponent"):
        pass

    def does_point_collide(self, point: "Vector2"):
        """주어진 좌표점이 이 엔티티와 '충돌'하는지 연산한다.
        
        `point`는 이 엔티티의 히트박스에 속하는 좌표점이어야 한다. 그렇지 않다면 항상 False를 반환한다.
        좌표점이 '충돌'한다는 것은, 이 엔티티에서 해당 점이 벽과 같은 충돌 판정을 가진다는 뜻이다.
        """
        return False

class Ladder(StaticEntity):
    def on_physics_trigger(self, phys: "PhysicsComponent"):
        ent = phys.owner
        if not ent.is_player: return
        assert isinstance(ent, Player)
        ent.on_ladder = 2

class Stair(StaticEntity):
    """계단. 닿는 물리력 있는 물체를 위로 올린다.
    
    to_left가 True라면, 계단은 왼쪽 위로 향한다. 아니라면 오른쪽 위를 향한다.

    ```
    to_left   not to_left
      ##             ##
      ####         ####
    ```
    """
    def __init__(self, to_left: bool):
        super().__init__()
        self._to_left = to_left
        self._width = TILE_SIZE
        self._height = TILE_SIZE
        self._built_rects = False

    
    @property
    def hitbox(self):
        self._build_rects()
        return self._higher_rect

    def _build_rects(self):
        if self._built_rects: return
        self._built_rects = True
        # 계단을 구성하는 두 개의 직사각형 중 위쪽 부분
        #   []
        # [][]
        self._higher_rect = Rect(self.position, (self._width // 2 - 2, self._height // 2))
        if not self._to_left:
            self._higher_rect.move_ip(self._width // 2 + 2, 0)

    def on_physics_trigger(self, phys: "PhysicsComponent"):
        self._build_rects()
        their_hitbox: "Rect | None" = phys.owner.get("hitbox")
        if not their_hitbox: return
        higher_rect = self._higher_rect
        # 위치를 높이고 아래 방향으로의 속도를 제거한다
        # 즉, 위쪽으로 수직 항력을 가한다

        if their_hitbox.colliderect(higher_rect):
            if their_hitbox.bottom - higher_rect.top <= PHYSICS_STAIR_HEIGHT:
                phys.owner.position.y = min(phys.owner.position.y, higher_rect.top)
                phys.velocity.y = min(0, phys.velocity.y)

        if DEBUG_DRAW_HITBOX:
            debug.draw_rect(higher_rect, on_map=True)
    
    def does_point_collide(self, point: "Vector2"):
        self._build_rects()
        return self._higher_rect.collidepoint(point)


class Spike(StaticEntity):
    _damage = 50

    def __init__(self, direction: "int" = 2):
        """direction 인수는 가시가 박힌 방향이다.
        
        방향은 숫자로 나타내는데, 키보드의 숫자 패드 모양에서 따온다.
        ```
        789
        456
        123
        ```

        따라서, direction이 8이면 천장에 박힌 가시, 2면 바닥에 박힌 가시,
        4면 왼쪽벽에 박힌 가시, 6이면 오른쪽벽에 박힌 가시이다.
        """
        super().__init__()

        if direction == 8:
            self._hitbox = Rect(0, 0, 60, 35)
        elif direction == 4:
            self._hitbox = Rect(0, 0, 35, 60)
        elif direction == 6:
            self._hitbox = Rect(25, 0, 35, 60)
        else:
            assert direction == 2, "direction must be one of [2,4,6,8]"
            self._hitbox = Rect(0, 25, 60, 35)

    @property
    def hitbox(self):
        return self._hitbox.move(self.position)

    def on_physics_trigger(self, phys: "PhysicsComponent"):
        phys.owner.call("take_damage", self._damage, self.hitbox.center)

class BoostTile(StaticEntity):
    def __init__(self, boost: float=1):
        super().__init__()
        self._boost = boost

class Door(StaticEntity):
    def __init__(self):
        super().__init__()

    def on_physics_trigger(self, phys: "PhysicsComponent"):
        if not phys.owner.is_player: return

        from scene_manager import SceneManager
        from scenes import GameScene
        scene = SceneManager.current_scene
        assert isinstance(scene, GameScene)
        scene.victory()

class BossDoor(Door):
    pass

class HpAdd(StaticEntity):
    AddHp = 100

    def surface(self):
        return ResourceLoader.load_image("item/life.png")
    
    def on_physics_trigger(self, phys: "PhysicsComponent"):
        if phys.owner.is_player:
            phys.owner.call("gain_hp", self.AddHp)
            self.remove()
