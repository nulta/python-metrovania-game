import pygame
import game_globals
from input_manager import *
from resource_loader import ResourceLoader
from .entity import *

F = PLAYER_MASS*PLAYER_VELOCITY*PLAYER_VELOCITY/2

class Player(Entity):
    def __init__(self, gender: int):
        super().__init__()
        self._hp = 200
        self._gender = gender
        self._move_speed = PLAYER_MOVE_SPEED
        self._weapon = None
        self._pivot = Vector2(15, 15)

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
        move_velocity = Vector2(axis * speed * game_globals.delta_time, 0)
        self.position += move_velocity

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

        return ResourceLoader.load_image(image_path)

    def _shoot(self):
        pass

    def _jump(self):
        pass

    def take_damage(self, damage):
        #지정된 양만큼의 데미지를 입는다.
        self.hp -= damage