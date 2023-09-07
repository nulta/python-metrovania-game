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
        self.physics = PhysicsComponent(self, )
        self._hp = 200
        self._gender = game_globals.player_gender
        self._move_speed = PLAYER_MOVE_SPEED
        self._jump_power = 500  # Max velocity when jumping. pixels per second.
        self._weapon = None
        self._pivot = Vector2(30, 56)
        self._walking = False
        self._flip = False
        self._focus_index = 0
        self._jump_timer=0
        self._max_jump_time=0.2
        self._jumping = False

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
        # TODO: 계단에서 점프할수 있게 하기


        if InputManager.pressed(ACTION_JUMP) and self.is_on_floor():
            self._jumping = True
            self._jump_timer = 0
        
        if InputManager.held(ACTION_JUMP) and self._jumping:
            self._jump_timer += game_globals.delta_time
            if self._jump_timer < self._max_jump_time:
                self.physics.velocity.y = min(self.physics.velocity.y, -self._jump_power)
        else:
            self._jumping = False
            if InputManager.released(ACTION_JUMP):
                print("Held jump button for:", self._jump_timer)


        # 물리 처리
        self.physics.update()
        if InputManager.pressed(ACTION_CHANGE_RIGHT):
            Audio.common.select()
            self._focus_index += 1
        elif InputManager.pressed(ACTION_CHANGE_LEFT):
            Audio.common.select()
            self._focus_index -= 1
        if InputManager.pressed(ACTION_SHOOT):
            pass

        # 카메라 이동
        camera_size = Vector2(GAME_WINDOW_SIZE)
        current_screen_idx = Vector2(self.position.x // camera_size.x, self.position.y // camera_size.y)
        current_screen_pos = Vector2(current_screen_idx.x * camera_size.x, current_screen_idx.y * camera_size.y)
        game_globals.camera_offset = current_screen_pos

    def surface(self):
        super().surface()

        image_offset_y = 0
        image_flipped = self._flip

        # 가져와야 할 이미지의 이름을 조립한다
        image_path = "sprites/player"
        if self._gender == GENDER_MALE:
            image_path += "/male"
        else:
            image_path += "/female"

        image_path += "/" + (self._weapon or "idle")

        if self._walking:
            from scene_manager import SceneManager
            time = SceneManager.scene_time
            idx = int(time // 0.25 % 4)
            if idx == 3: idx = 1
            if idx == 1:
                image_offset_y = 2
            image_path += f"_{idx}"
        else:
            image_path += "_1"

        image_path += ".png"

        surface = ResourceLoader.load_image_2x(image_path)
        surface = pygame.transform.flip(surface, image_flipped, False)
        surface.scroll(0, image_offset_y)

        return surface

    def take_damage(self, damage):
        #지정된 양만큼의 데미지를 입는다.
        self.hp -= damage

    def is_on_floor(self):
        """바닥에 발을 딛고 있는가?"""
        down_1px = Vector2(0, 1)
        check_points = [
            Vector2(self.hitbox.bottomleft) + down_1px,
            Vector2(self.hitbox.midbottom) + down_1px,
            Vector2(self.hitbox.bottomright) + down_1px,
        ]
        return any(map(self.physics.does_point_collide, check_points))
