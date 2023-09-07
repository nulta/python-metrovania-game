from .entity import Entity
import pygame
from .components.physics_component import PhysicsComponent
from constants import TILE_SIZE
import debug

class StaticEntity(Entity):
    is_static = True

    @property
    def hitbox(self):
        size = pygame.Vector2(60, 60)
        return pygame.Rect(self.position, size)
    
    def on_physics_trigger(self, phys: "PhysicsComponent"):
        pass

    def does_point_collide(self, point: "pygame.Vector2"):
        """주어진 좌표점이 이 엔티티와 '충돌'하는지 연산한다.
        
        `point`는 이 엔티티의 히트박스에 속하는 좌표점이어야 한다. 그렇지 않다면 항상 False를 반환한다.
        좌표점이 '충돌'한다는 것은, 이 엔티티에서 해당 점이 벽과 같은 충돌 판정을 가진다는 뜻이다.
        """
        return False

class Ladder(StaticEntity):
    pass

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

    def _build_rects(self):
        if self._built_rects: return
        self._built_rects = True
        # 계단을 구성하는 두 개의 직사각형
        #   []
        # [][]
        self._higher_rect = pygame.Rect(self.position, (self._width // 2, self._height))
        self._lower_rect = pygame.Rect(self.position, (self._width // 2, self._height // 2)).move(0, self._height // 2)
        if self._to_left:
            self._lower_rect.move_ip(self._width // 2, 0)
        else:
            self._higher_rect.move_ip(self._width // 2, 0)


    def on_physics_trigger(self, phys: "PhysicsComponent"):
        self._build_rects()
        their_hitbox: "pygame.Rect | None" = phys.owner.get("hitbox")
        if not their_hitbox: return
        higher_rect = self._higher_rect
        lower_rect = self._lower_rect
        
        # 위치를 높이고 아래 방향으로의 속도를 제거한다
        # 즉, 위쪽으로 수직 항력을 가한다
        if their_hitbox.colliderect(higher_rect):
            # 계단의 높은 지점을 즈려밟고 있다
            phys.owner.position.y = min(phys.owner.position.y, higher_rect.top)
            phys.velocity.y = min(0, phys.velocity.y)
            debug.draw_point(higher_rect.center, on_map=True)
        elif their_hitbox.colliderect(lower_rect):
            # 계단의 낮은 지점을 즈려밟고 있다
            phys.owner.position.y = min(phys.owner.position.y, lower_rect.top)
            phys.velocity.y = min(0, phys.velocity.y)
            debug.draw_point(lower_rect.center, on_map=True)

        debug.draw_rect(higher_rect, on_map=True)
        debug.draw_rect(lower_rect, on_map=True)
    
    def does_point_collide(self, point: "pygame.Vector2"):
        self._build_rects()
        return self._lower_rect.collidepoint(point) or self._higher_rect.collidepoint(point)



class Spike(StaticEntity):
    pass

class BoostTile(StaticEntity):
    def __init__(self, boost: float=1):
        super().__init__()
        self._boost = boost
