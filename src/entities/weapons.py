from .entity import Entity
from .player import Player
from .bullet import Bullet, BulletInfo
from pygame import Vector2
from pygame import Rect
from constants import *
from typing import final
from resource_loader import ResourceLoader

class Weapon:
    shoot_cooldown = 0
    player_graphic: "str | None" = None

    def __init__(self, is_enemy=True):
        self._last_shoot_time = 0
        self._is_enemy = is_enemy

    def on_shoot(self, direction: "Vector2"):
        pass

    def can_shoot(self, direction: "Vector2"):
        from scene_manager import SceneManager
        time = SceneManager.scene_time
        since_last_shoot = time - self._last_shoot_time
        return since_last_shoot >= self.shoot_cooldown
    
    @final
    def shoot(self, direction: "Vector2"):
        from scene_manager import SceneManager
        direction = direction.normalize()

        if not self.can_shoot(direction):
            return
        self.on_shoot(direction)
        self._last_shoot_time = SceneManager.scene_time

class BasicGun(Weapon):
    shoot_cooldown = 1.0
    player_graphic = None

    _bullet_info = BulletInfo()
    _bullet_info.damage = 5
    _bullet_info.lifetime = 2
    _bullet_info.rect = Rect(0, 0, 10, 10)
    # _bullet_info.surface = ResourceLoader.load_image_2x("?")
    
    _bullet_speed = 500

    def _fire_bullet(self, direction: "Vector2"):
        Bullet(self._bullet_info, direction * self._bullet_speed, self._is_enemy)

    def on_shoot(self, direction):
        self._fire_bullet(direction)
        # TODO: 소리 재생
