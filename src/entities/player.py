import pygame
import game_globals
from input_manager import InputManager
from resource_loader import ResourceLoader
from .entity import *
from pygame.math import Vector2

F = PLAYER_MASS*PLAYER_VELOCITY*PLAYER_VELOCITY/2

class Player(Entity):
    is_player = True

    def __init__(self, gender: int):
        super().__init__()
        self._hp = 200
        self._gender = gender
        self._move_speed = PLAYER_MOVE_SPEED
        self._weapon = None
        self._pivot = Vector2(15, 15)
        self.isJump = 0
        self.v = PLAYER_VELOCITY
        self.m = PLAYER_MASS


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

        return ResourceLoader.load_image_2x(image_path)


    def _shoot(self):
        pass

    def _jump(self):
        if self.isJump >0:
            self._pivot = Vector2(15, 30)
            if self.isJump ==2:
                self.v = PLAYER_VELOCITY
            if self.v >0:
                F = 0.5*self.m*(self.v*self.v)
            else:
                F = 0.5*self.m*(self.v*self.v)*(-1)
            self.position.y -= round(F)
            self.v -= 1
            if self._position.y > GAME_WINDOW_SIZE[1]:
                self._position.y = GAME_WINDOW_SIZE[1]
                self.isJump =0
                self.v = PLAYER_VELOCITY
        self._pivot = Vector2(15, 15)

    def take_damage(self, damage):
        #지정된 양만큼의 데미지를 입는다.
        self.hp -= damage
    def get_x_position(self):
        return self.position.x
    def get_y_position(self):

        return self.position.y