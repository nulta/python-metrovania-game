import pygame
import game_globals
import debug
from pygame.math import Vector2
from input_manager import InputManager
from resource_loader import ResourceLoader
from .entity import Entity
from constants import *
from .components.physics_component import PhysicsComponent

class Player(Entity):
    is_player = True

    def __init__(self, gender: int):
        super().__init__()
        self.physics = PhysicsComponent(self, )
        self._hp = 200
        self._gender = gender
        self._move_speed = PLAYER_MOVE_SPEED
        self._max_jump_power = 600
        self._weapon = None
        self._pivot = Vector2(30, 56)

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
        # move_velocity = Vector2(axis * speed * game_globals.delta_time, 0)
        # self.position += move_velocity
        self.physics.velocity.x = axis * speed

        # 점프 처리
        # TODO: 바닥에 붙어있을 경우에만 점프 가능하게 하기
        # TODO: 약한점프 강한점프 구분하게 하기 (누르는 시간에 따라서)
        if InputManager.pressed(ACTION_JUMP):
            self.physics.velocity.y = -self._max_jump_power

        # 물리 처리
        self.physics.update()
        debug.rect(self.hitbox)
        # debug.point(self.position)
    def surface(self):
        super().surface()

        # 가져와야 할 이미지의 이름을 조립한다
        image_path = "sprites/player"
        if self._gender == GENDER_MALE:
            image_path += "/male"
        else:
            image_path += "/female"

        image_path += "/" + (self._weapon or "idle")
        image_path += ".png"

        return ResourceLoader.load_image_2x(image_path)
    def take_damage(self, damage):
        #지정된 양만큼의 데미지를 입는다.
        self.hp -= damage



