import pygame
import game_globals
import debug
from pygame.math import Vector2
from input_manager import InputManager
from resource_loader import ResourceLoader
import util
from .entity import Entity
from constants import *
from .components.physics_component import PhysicsComponent
from audio import Audio
from . import weapons
from .character_base import CharacterBase

class Player(CharacterBase):
    is_player = True

    def __init__(self):
        super().__init__()
        self._gender = game_globals.player_gender

        self._max_hp = 200                          # 최대 체력
        self._damage_taking_delay = 2.0             # 데미지를 입은 뒤의 일시적 무적 시간(초)
        # self._move_speed = PLAYER_MOVE_SPEED        # 이동 속도
        # self._jump_power = 500                      # 점프 시의 최대 수직 속력 (px/s).
        # self._max_jump_time = 0.2                   # 긴 점프의 최대 유지 시간
        # self._max_damage_knockback = 3000           # 데미지 넉백의 최대 속력 (데미지 비례)
        # self._damage_knockback_y_multiplier = 1.5   # 데미지 넉백에서 Y방향 속력에 곱해질 수
        # self._x_velocity_dec_midair = 600           # 초당 x방향 속력의 감소량 (공중에 떴을 때)
        # self._x_velocity_dec_floor = 6000           # 초당 x방향 속력의 감소량 (땅 위에서)
        # self._x_velocity_dec_moving_mul = 3.0       # 이동 키를 누르고 있을 때, 초당 x방향 속력 감소량의 배수
        self._weapon = weapons.BasicGun(False)
        self._hp = self._max_hp


    def update(self):
        # 이동 커맨드 처리
        self._move_command.move_axis = InputManager.axis(AXIS_HORIZONTAL)
        self._move_command.jump = InputManager.held(ACTION_JUMP)
        self._move_command.shoot = InputManager.held(ACTION_SHOOT)
        if InputManager.pressed(ACTION_SHOOT):
            self._shoot_timer = 0
        
        # 업데이트
        super().update()

        # 카메라 이동
        camera_size = Vector2(GAME_WINDOW_SIZE)
        current_screen_idx = Vector2(self.position.x // camera_size.x, (self.position.y-2) // camera_size.y)
        current_screen_pos = Vector2(current_screen_idx.x * camera_size.x, current_screen_idx.y * camera_size.y)
        game_globals.camera_offset = current_screen_pos

    def surface(self):
        weapon_name = "idle"
        if self._weapon and self._weapon.player_graphic:
            weapon_name = self._weapon.player_graphic

        if self._gender == GENDER_MALE:
            self._sprite_name = f"player/male/{weapon_name}"
        else:
            self._sprite_name = f"player/female/{weapon_name}"
        
        return super().surface()

    def take_damage(self, damage: "int", origin: "Vector2 | None" = None):
        took_damage = super().take_damage(damage, origin)
        if took_damage:
            Audio.play("hurt_2")
        return took_damage
    
    def gain_hp(self, gain: "int"):
        """player의 hp가 추가된다"""
        self.hp += gain

    def slow_speed(self,slow:"int"):
        self._move_speed -=slow

    def jump(self, long_jump=False):
        jumped = super().jump(long_jump)
        if jumped:
            Audio.play("jump_1")
        return jumped

    def _on_die(self):
        from scene_manager import SceneManager
        from scenes.gameover_scene import GameOverScene
        super()._on_die()

        SceneManager.push_scene(GameOverScene())
