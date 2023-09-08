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

class Player(Entity):
    is_player = True

    def __init__(self):
        super().__init__()
        self.physics = PhysicsComponent(self)

        self._max_hp = 200                          # 최대 체력
        self._damage_taking_delay = 2.0             # 데미지를 입은 뒤의 일시적 무적 시간(초)
        self._gender = game_globals.player_gender   # 성별값
        self._move_speed = PLAYER_MOVE_SPEED        # 이동 속도
        self._jump_power = 500                      # 점프 시의 최대 수직 속력 (px/s).
        self._max_jump_time = 0.2                   # 긴 점프의 최대 유지 시간

        self._weapon = weapons.BasicGun(False)
        self._hp = self._max_hp
        self._pivot = Vector2(30, 56)
        self._walking = False
        self._flip = False
        self._jump_timer = 0
        self._jumping = False
        self._invincible_timer = 0  # 무적 타이머. 0보다 큰 값이면 무적 상태임을 뜻한다.
        self._shoot_timer = 0       # 무기 발사 타이머. 발사 키를 "꾹 누르고 있을 때의" 연사 처리용.

    @property
    def hitbox(self):
        offset = pygame.Vector2(-20, -56)
        size = pygame.Vector2(40, 56)
        return pygame.Rect(self.position + offset, size)

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        if value < 0:
            value = 0
        self._hp = value

    def update(self):
        super().update()
        dt = game_globals.delta_time

        # 좌우 이동 처리
        axis = InputManager.axis(AXIS_HORIZONTAL)
        speed = self._move_speed
        if axis:
            self.physics.velocity.x = axis * speed
            self._walking = True
            if axis > 0:
                self._flip = True
            else:
                self._flip = False
        else:
            self.physics.velocity.x = 0
            self._walking = False

        # 점프 처리
        if InputManager.pressed(ACTION_JUMP) and self.is_on_floor():
            self._jumping = True
            self._jump_timer = 0

        if InputManager.held(ACTION_JUMP) and self._jumping:
            self._jump_timer += dt
            if self._jump_timer < self._max_jump_time:
                self.physics.velocity.y = min(self.physics.velocity.y, -self._jump_power)
        else:
            self._jumping = False

        # 물리 처리
        self.physics.update()

        # 무기 처리
        if self._weapon:
            self._weapon.position = Vector2(self.hitbox.center)
            self._weapon.direction = Vector2(1 if self._flip else -1, 0)
            if InputManager.pressed(ACTION_SHOOT):
                self._shoot_timer = self._weapon.shoot_cooldown
                self._weapon.shoot()
            elif InputManager.held(ACTION_SHOOT):
                self._shoot_timer -= dt
                if self._shoot_timer <= 0:
                    self._shoot_timer = self._weapon.shoot_cooldown
                    self._weapon.shoot()
            else:
                self._shoot_timer = 0
        
        # 무적 상태 처리
        self._invincible_timer = max(0, self._invincible_timer - dt)

        # 카메라 이동
        camera_size = Vector2(GAME_WINDOW_SIZE)
        current_screen_idx = Vector2(self.position.x // camera_size.x, self.position.y // camera_size.y)
        current_screen_pos = Vector2(current_screen_idx.x * camera_size.x, current_screen_idx.y * camera_size.y)
        game_globals.camera_offset = current_screen_pos

    def surface(self):
        from scene_manager import SceneManager
        scene_time = SceneManager.scene_time

        image_offset_y = 0
        image_flipped = self._flip

        # 가져와야 할 이미지의 이름을 조립한다
        image_path = "sprites/player"
        if self._gender == GENDER_MALE:
            image_path += "/male"
        else:
            image_path += "/female"

        image_path += "/" + (self._weapon.player_graphic or "idle")

        if self._walking:
            idx = int(scene_time // 0.25 % 4)
            if idx == 3: idx = 1
            if idx == 1: image_offset_y = 2
            image_path += f"_{idx}"
        else:
            image_path += "_1"

        image_path += ".png"

        surface = ResourceLoader.load_image_2x(image_path).copy()
        surface = pygame.transform.flip(surface, image_flipped, False)
        surface.scroll(0, image_offset_y)

        # 무적상태일 경우 깜빡임
        if self._invincible_timer:
            is_in_blink = scene_time * 10 % 2 > 1
            if is_in_blink:
                # 반투명 상태로 만든다.
                surface.set_alpha(128)

        return surface

    def take_damage(self, damage: "int"):
        """지정된 양만큼의 데미지를 입는다."""

        # 무적 상태일 때는 데미지를 받지 않는다.
        if self._invincible_timer:
            return

        # 데미지를 입은 뒤에는 일시적으로 무적이 된다.
        self._invincible_timer = self._damage_taking_delay
        self.hp -= damage
        print(str(self), "HP ->", self.hp)

    def is_on_floor(self):
        """바닥에 발을 딛고 있는가?"""
        down_1px = Vector2(0, 1)
        check_points = [
            Vector2(self.hitbox.bottomleft) + down_1px,
            Vector2(self.hitbox.midbottom) + down_1px,
            Vector2(self.hitbox.bottomright) + down_1px,
        ]
        return any(map(self.physics.does_point_collide, check_points))
