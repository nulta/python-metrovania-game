from entities.components.physics_component import PhysicsComponent
from .entity import Entity
import pygame
from pygame import Rect, Vector2
from .components.physics_component import PhysicsComponent
from constants import TILE_SIZE, PHYSICS_STAIR_HEIGHT, DEBUG_DRAW_HITBOX
import debug
from resource_loader import ResourceLoader
from .player import *
from scene_manager import SceneManager
import game_globals
from .weapons import *


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
        if not ent.is_player:
            return
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
        if self._built_rects:
            return
        self._built_rects = True
        # 계단을 구성하는 두 개의 직사각형 중 위쪽 부분
        #   []
        # [][]
        self._higher_rect = Rect(
            self.position, (self._width // 2 - 2, self._height // 2)
        )
        if not self._to_left:
            self._higher_rect.move_ip(self._width // 2 + 2, 0)

    def on_physics_trigger(self, phys: "PhysicsComponent"):
        self._build_rects()
        their_hitbox: "Rect | None" = phys.owner.get("hitbox")
        if not their_hitbox:
            return
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
            self._hitbox = Rect(0, 9, 60, 20)
        elif direction == 4:
            self._hitbox = Rect(9, 0, 20, 60)
        elif direction == 6:
            self._hitbox = Rect(31, 0, 20, 60)
        else:
            assert direction == 2, "direction must be one of [2,4,6,8]"
            self._hitbox = Rect(0, 31, 60, 20)

    @property
    def hitbox(self):
        return self._hitbox.move(self.position)

    def on_physics_trigger(self, phys: "PhysicsComponent"):
        phys.owner.call("take_damage", self._damage, self.hitbox.center)


class BoostTile(StaticEntity):
    def __init__(self, boost: float = 1):
        super().__init__()
        self._boost = boost

    @property
    def hitbox(self):
        return Rect(0, 20, 60, 20).move(self.position)

    def on_physics_trigger(self, phys: "PhysicsComponent"):
        phys.velocity.x += self._boost * 6000 * game_globals.delta_time
        phys.velocity.x = util.clamp(phys.velocity.x, -900, 900)


class Door(StaticEntity):
    def __init__(self):
        super().__init__()

    def surface(self):
        return ResourceLoader.load_image_2x("item/door.png")

    def on_physics_trigger(self, phys: "PhysicsComponent"):
        if not phys.owner.is_player:
            return

        from entity_manager import EntityManager

        scene = EntityManager.game_scene
        assert scene
        scene.victory()


class BossDoor(Door):
    pass


class HpAdd(StaticEntity):
    AddHp = 50

    def surface(self):
        return ResourceLoader.load_image_2x("item/life.png")

    def on_physics_trigger(self, phys: "PhysicsComponent"):
        if phys.owner.is_player:
            phys.owner.call("gain_hp", self.AddHp)
            self.remove()


class Fire(StaticEntity):
    _damage = 10

    def surface(self):
        # 가져와야 할 이미지의 이름을 조립한다
        chip_idx = int((SceneManager.scene_time * 7) % 2)
        image_path = f"item/fire_{chip_idx}.png"
        return ResourceLoader.load_image_2x(image_path).copy()
    def on_physics_trigger(self, phys: "PhysicsComponent"):
            phys.owner.call("take_damage", self._damage, self.hitbox.center)


class Wind(StaticEntity):
    def surface(self):
        # 가져와야 할 이미지의 이름을 조립한다
        chip_idx = int(SceneManager.scene_time * 7 % 2)
        image_path = f"item/wind_{chip_idx}.png"

        return ResourceLoader.load_image_2x(image_path).copy()

    def on_physics_trigger(self, phys: "PhysicsComponent"):
        phys.velocity.y -= 600 * game_globals.delta_time
        phys.velocity.y = util.clamp(phys.velocity.y, -600, 0)


class Electric_ball(StaticEntity):
    _damage = 50

    @property
    def hitbox(self):
        return Rect(self.position, (40, 40))

    def surface(self):
        # 가져와야 할 이미지의 이름을 조립한다
        chip_idx = int((SceneManager.scene_time * 5) % 2)
        image_path = f"item/electric_{chip_idx}.png"

        return ResourceLoader.load_image_2x(image_path).copy()

    def on_physics_trigger(self, phys: "PhysicsComponent"):
        phys.owner.call("take_damage", self._damage, self.hitbox.center)


class Electric_box(StaticEntity):
    _damage = 50

    def surface(self):
        chip_idx = int((SceneManager.scene_time * 5) % 2)
        image_path = f"item/electric_box_{chip_idx}.png"

        return ResourceLoader.load_image_2x(image_path).copy()

    def on_physics_trigger(self, phys: "PhysicsComponent"):
        phys.owner.call("take_damage", self._damage, self.hitbox.center)


class MovingBoard(StaticEntity):
    @property
    def hitbox(self):
        return Rect(self.position + Vector2(0, 20), (60, 32))

    def surface(self):
        image_path = f"item/moving_side.png"
        return ResourceLoader.load_image_2x(image_path).copy()

    def update(self):
        if game_globals.game_time % 10 < 5:
            self.position.x -= 55 * game_globals.delta_time
        elif game_globals.game_time % 10 >= 5:
            self.position.x += 55 * game_globals.delta_time

    def on_physics_trigger(self, phys: "PhysicsComponent"):
        phys.owner.position.y = min(phys.owner.position.y, self.hitbox.top)
        phys.velocity.y = min(0, phys.velocity.y)

    def does_point_collide(self, point: "Vector2"):
        return self.hitbox.collidepoint(point)


class Fire_time1(StaticEntity):
    _damage = 10

    def __init__(self):
        super().__init__()
        self._active = True

    def update(self):
        super().update()
        self._active = SceneManager.scene_time % 4 < 2

    def surface(self):
        if not self._active:
            return pygame.Surface((0,0))

        # 가져와야 할 이미지의 이름을 조립한다
        chip_idx = int((SceneManager.scene_time * 7) % 2+2)
        image_path = f"item/fire_top_{chip_idx}.png"

        return ResourceLoader.load_image_2x(image_path).copy()

    def on_physics_trigger(self, phys: "PhysicsComponent"):
        if self._active:
            phys.owner.call("take_damage", self._damage, self.hitbox.center)

class Fire_time2(StaticEntity):
    _damage = 10

    def __init__(self):
        super().__init__()
        self._active = True

    def update(self):
        super().update()
        self._active = SceneManager.scene_time % 4 >= 2

    def surface(self):
        if not self._active:
            return pygame.Surface((0,0))

        # 가져와야 할 이미지의 이름을 조립한다
        chip_idx = int((SceneManager.scene_time * 7) % 2)
        image_path = f"item/fire_top_{chip_idx}.png"

        return ResourceLoader.load_image_2x(image_path).copy()

    def on_physics_trigger(self, phys: "PhysicsComponent"):
        if self._active:
            phys.owner.call("take_damage", self._damage, self.hitbox.center)