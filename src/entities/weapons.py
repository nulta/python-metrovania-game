from audio import Audio
from .bullet import Bullet, WindBullet, BulletInfo, GrenadeEntity
from pygame import Vector2
from pygame import Rect
from constants import *
from typing import final
from resource_loader import ResourceLoader
import random

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
        """
        이 무기가 발사될 방향을 나타내는 방향 벡터. 
        
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
    player_graphic = None

    shoot_cooldown = 0.3
    _bullet_speed = 600

    _bullet_info = BulletInfo()
    _bullet_info.damage = 50
    _bullet_info.lifetime = 1000 / _bullet_speed  # 1000px를 가는 데 걸리는 시간만큼
    _bullet_info.rect = Rect(0, 0, 20, 20)
    _bullet_info.sprite = "item/bullet.png"


    def _fire_bullet(self):
        bullet = Bullet(self._bullet_info, self.direction * self._bullet_speed, self._is_enemy)
        bullet.position = self.position

    def on_shoot(self):
        self._fire_bullet()
        Audio.play("gun_2")

class FireBossGun(BasicGun):
    shoot_cooldown = 1.2
    _bullet_speed = 300

    _bullet_info = BulletInfo()
    _bullet_info.damage = 50
    _bullet_info.lifetime = 1000 / _bullet_speed  # 1000px를 가는 데 걸리는 시간만큼
    _bullet_info.rect = Rect(0, 0, 20, 20)
    _bullet_info.sprite = "item/firebullet.png"

    def on_shoot(self):
        self._fire_bullet()
        Audio.play("gun_1")


class WindBossGun1(BasicGun):
    shoot_cooldown = 0.8
    _bullet_speed = 600

    _bullet_info = BulletInfo()
    _bullet_info.damage = 0
    _bullet_info.lifetime = 1000 / _bullet_speed
    _bullet_info.rect = Rect(0, 0, 60, 60)
    _bullet_info.sprite = "item/smoke_0.png"

    def _fire_bullet(self):
        bullet1 = WindBullet(self._bullet_info, self.direction * self._bullet_speed, self._is_enemy)
        bullet2 = WindBullet(self._bullet_info, self.direction * self._bullet_speed, self._is_enemy)
        bullet1.position = self.position + self.direction * 60
        bullet2.position = self.position

    def on_shoot(self):
        self._fire_bullet()
        Audio.play("wind_1")


class WindBossGun2(BasicGun):
    shoot_cooldown = 2
    _bullet_speed = 400

    _bullet_info = BulletInfo()
    _bullet_info.damage = 40
    _bullet_info.lifetime = 1000 / _bullet_speed
    _bullet_info.rect = Rect(0, 0, 60, 60)
    _bullet_info.sprite = "item/poison_smoke_1.png"

    def _fire_bullet(self):
        bullet1 = Bullet(self._bullet_info, self.direction * self._bullet_speed, self._is_enemy)
        bullet2 = Bullet(self._bullet_info, self.direction * self._bullet_speed, self._is_enemy)
        bullet3 = Bullet(self._bullet_info, self.direction * self._bullet_speed, self._is_enemy)
        bullet4 = Bullet(self._bullet_info, self.direction * self._bullet_speed, self._is_enemy)
        
        offset = random.choice([0, -60])
        bullet1.position = self.position + Vector2(0, offset)
        bullet2.position = self.position + Vector2(0, -220 + offset)
        bullet3.position = self.position + Vector2(0, -280 + offset)
        bullet4.position = self.position + Vector2(0, (-340 + offset) % -400)

    def on_shoot(self):
        self._fire_bullet()
        Audio.play("wind_2")

class WindBossGun3(BasicGun):
    """난사 패턴!"""
    shoot_cooldown = 1

    def on_shoot(self):
        gun = None
        if random.randint(0,1) == 0:
            gun = WindBossGun1(self._is_enemy)
        else:
            gun = WindBossGun2(self._is_enemy)

        gun.position = self.position
        gun.direction = self.direction
        gun.shoot()


class GrenadeBossGun(BasicGun):
    shoot_cooldown = 0.2

    def _fire_bullet(self):
        rand_dir = Vector2(random.random()*2-1, random.random()*2-1).normalize()
        nade_vel = rand_dir * random.randint(600, 1800)
        nade = GrenadeEntity()
        nade.position = self.position
        nade.physics.velocity = nade_vel

    def on_shoot(self):
        self._fire_bullet()
        Audio.play("throw")


class PoorGun(BasicGun):
    # 잡몹이 들 기본 무기.

    shoot_cooldown = 0.7
    _bullet_speed = 700

    _bullet_info = BulletInfo()
    _bullet_info.damage = 40
    _bullet_info.lifetime = 1000 / _bullet_speed
    _bullet_info.rect = Rect(0, 0, 20, 20)
    _bullet_info.sprite = "item/bullet.png"

    def on_shoot(self):
        self._fire_bullet()
        Audio.play("gun_3")
