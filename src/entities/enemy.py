import random
import pygame
from .entity import *
from .player import *
from .weapons import *
import time
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


    def update(self):
        self._move_command.move_axis = 1  # TODO
        super().update()



class FireEnemy(Enemy):

    def __init__(self):
        super().__init__()
        self._sprite_name = "enemy/fire"
        self._weapon = BasicGun(True)


    def update(self):
        super().update()

