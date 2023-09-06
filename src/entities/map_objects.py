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

    def on_physics_trigger(self, phys: "PhysicsComponent"):
        their_hitbox: "pygame.Rect | None" = phys.owner.get("hitbox")
        if not their_hitbox: return

        # 계단을 구성하는 두 개의 직사각형
        #   []
        # [][]
        higher_rect = pygame.Rect(self.position, (self._width // 2, self._height))
        lower_rect = pygame.Rect(self.position, (self._width // 2, self._height // 2)).move(0, self._height // 2)
        if self._to_left:
            lower_rect.move_ip(self._width // 2, 0)
        else:
            higher_rect.move_ip(self._width // 2, 0)
        
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
        


class Spike(StaticEntity):
    pass

class BoostTile(StaticEntity):
    def __init__(self, boost: float=1):
        super().__init__()
        self._boost = boost
