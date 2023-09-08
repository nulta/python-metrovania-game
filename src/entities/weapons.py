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
        self._position = Vector2(0, 0)
        self._direction = Vector2(0, 0)


    @property
    def position(self):
        """이 무기가 발사될 위치."""
        return self._position
    
    @position.setter
    def position(self, value: "Vector2"):
        self._position = value

    @property
    def direction(self):
        """이 무기가 발사될 방향을 나타내는 방향 벡터. 
        
        방향을 가지지만 크기는 항상 1인 단위벡터이다.
        """
        return self._direction
    
    @direction.setter
    def direction(self, value: "Vector2"):
        self._direction = value.normalize()


    def on_shoot(self) -> "None":
        """무기가 발사될 때 수행할 행동을 정의한다."""
        pass

    def can_shoot(self) -> "bool":
        """무기가 발사될 수 있는지 여부를 판단해서 반환한다."""
        from scene_manager import SceneManager
        time = SceneManager.scene_time
        since_last_shoot = time - self._last_shoot_time
        return since_last_shoot >= self.shoot_cooldown
    
    @final
    def shoot(self):
        """무기에 발사 명령을 내린다. 발사할 수 없다면 발사하지 않는다."""
        from scene_manager import SceneManager
        if not self.can_shoot(): return
        self.on_shoot()
        self._last_shoot_time = SceneManager.scene_time

class BasicGun(Weapon):
    shoot_cooldown = 0.1
    player_graphic = None

    _bullet_info = BulletInfo()
    _bullet_info.damage = 5
    _bullet_info.lifetime = 2
    _bullet_info.rect = Rect(0, 0, 20, 20)
    # _bullet_info.surface = ResourceLoader.load_image_2x("?")
    
    _bullet_speed = 600

    def _fire_bullet(self):
        print(repr(self), "Fire!")
        bullet = Bullet(self._bullet_info, self.direction * self._bullet_speed, self._is_enemy)
        bullet.position = self.position

    def on_shoot(self):
        self._fire_bullet()
        # TODO: 소리 재생
