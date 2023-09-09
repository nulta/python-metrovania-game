import random
import pygame
from .entity import *
from .player import *
from .weapons import *
import time
import math
from pygame import Surface
from pygame.math import Vector2
from constants import *
from .character_base import CharacterBase

class Enemy(CharacterBase):
    is_enemy = True

    def __init__(self):
        super().__init__()

        self._sprite_name = ""                             # sprites/enemy/{???}_1.png\
        # self._max_hp = 100                          # 최대 체력
        # self._damage_taking_delay = 1.0             # 데미지를 입은 뒤의 일시적 무적 시간(초)
        # self._move_speed = PLAYER_MOVE_SPEED        # 이동 속도
        # self._jump_power = 500                      # 점프 시의 최대 수직 속력 (px/s).
        # self._max_jump_time = 0.2                   # 긴 점프의 최대 유지 시간
        # self._max_damage_knockback = 3000           # 데미지 넉백의 최대 속력 (데미지 비례)
        # self._damage_knockback_y_multiplier = 1.5   # 데미지 넉백에서 Y방향 속력에 곱해질 수
        # self._x_velocity_dec_midair = 600           # 초당 x방향 속력의 감소량 (공중에 떴을 때)
        # self._x_velocity_dec_floor = 6000           # 초당 x방향 속력의 감소량 (땅 위에서)
        # self._x_velocity_dec_moving_mul = 3.0       # 이동 키를 누르고 있을 때, 초당 x방향 속력 감소량의 배수
        self._weapon = BasicGun(True)
        # self._hp = self._max_hp
        
        self._floor_check_distance = 30  # 앞에 바닥이 있는지 확인할 때, 확인지점의 거리(px)
        self._ai_ignore_distance = 500   # 플레이어가 이 거리보다 멀다면 보지 못한다
        self._ai_minimum_distance = 200   # 플레이어가 이 거리보다 가깝다면 뒤로 뺀다


    def update(self):
        self._update_command()
        super().update()

    def _update_command(self):
        """현재 시점에서 AI의 MoveCommand를 업데이트한다."""
        command = self._move_command
        command.reset()

        player_dist = self._get_distance_to_player()
        to_player_axis = self._get_axis_to_player()

        # 플레이어를 찾을 수 있는가?
        if player_dist >= self._ai_ignore_distance:
            return

        # 좀 뒤로 이동해야 하는가?
        if player_dist <= self._ai_minimum_distance:
            command.move_axis = -to_player_axis
        
        # 이동할 방향이 안전한가?
        if not self._is_okay_to_go(command.move_axis):
            command.move_axis = 0.0

        # 이동하지 않고 있는가?
        if command.move_axis == 0:
            # 플레이어 쪽을 바라보고 총을 쏜다.
            command.move_axis = to_player_axis * 0.05
            command.shoot = True


    def _get_distance_to_player(self):
        """플레이어와의 거리를 받아온다. 플레이어가 없다면 무한대를 반환한다."""
        from entity_manager import EntityManager
        player = EntityManager.get_player()

        if not player:
            return float("inf")
        else:
            return self.position.distance_to(player.position)
        
    def _get_axis_to_player(self):
        """플레이어 쪽으로 향하는 axis를 받아온다. 플레이어가 없거나 위치가 일치한다면 0을 반환한다."""
        from entity_manager import EntityManager
        player = EntityManager.get_player()

        if not player:
            return 0.0
        else:
            diff = player.position.x - self.position.x
            if diff == 0:
                return 0.0
            else:
                return math.copysign(1.0, diff)

    def _is_okay_to_go(self, axis: "float"):
        """이 앞 axis쪽 방향에 벽과 낭떠러지가 없는지 체크한다."""
        collides = self.physics.does_point_collide
        distance = self._floor_check_distance

        to_wall = self.hitbox.midtop + Vector2(axis * distance, 0)
        to_floor_1 = self.hitbox.midbottom + Vector2(axis * distance, 1)
        to_floor_2 = self.hitbox.midbottom + Vector2(axis * distance, 31)
        return not collides(to_wall) and (collides(to_floor_1) or collides(to_floor_2))

<<<<<<< HEAD
class BasicEnemy(Enemy):

=======
class FireEnemy(Enemy):
>>>>>>> 7fa1e7b3fc7ef42e57fce73e4cdbe2c4cf413e20
    def __init__(self):
        super().__init__()
        self._sprite_name = "enemy/fire"
        self._weapon = PoorGun(True)


    def update(self):
        super().update()

