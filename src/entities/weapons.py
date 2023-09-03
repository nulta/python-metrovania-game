from .entity import *
from .player import *
from .enemy import *
from pygame.math import Vector2
from constants import *
from typing import final

class Weapon:
    shoot_cooldown = 0
    player_graphic: "str | None" = None

    def __init__(self):
        self._last_shoot_time = 0

    def on_shoot(self):
        pass

    def can_shoot(self):
        from scene_manager import SceneManager
        time = SceneManager.scene_time
        since_last_shoot = time - self._last_shoot_time
        return since_last_shoot >= self.shoot_cooldown
    
    @final
    def shoot(self):
        from scene_manager import SceneManager
        if not self.can_shoot():
            return
        self.on_shoot()
        self._last_shoot_time = SceneManager.scene_time

class BasicGun(Weapon):
    shoot_cooldown = 1.0
    player_graphic = None

    def on_shoot(self):
        return super().on_shoot()
