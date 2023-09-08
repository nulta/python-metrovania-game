import random
import pygame
from .entity import *
from .player import *
from .weapons import *
import time
from pygame import Surface
from pygame.math import Vector2
from constants import *

class Enemy(Entity):
    def __init__(self):
        super().__init__()
        self._hp = 100
        self._move_speed = 10
        self._next_attack = 2  # 초 단위

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
        # AI 처리, 이동 처리, 기타 등등...
        from entity_manager import EntityManager
        player = EntityManager.get_player()
        if not player: return  
        if self.position.x <= player.position.x:
            self.position.x += 1
        elif self. position.x>= player.position.x:
            self.position.x -=1
        
        self._next_attack -= game_globals.delta_time
        if self._next_attack <= 0:
            self._next_attack = random.randint(1, 3)
            self.attack()

        
        

    def surface(self,enemy_name):
        super().surface()
        # 적의 모습을 화면에 그린다.
        image_path = RESOURCE_PATH + "/enemy/"
        image_path += enemy_name
        image_path += ".png"
        # 조립한 이미지 이름대로, 불러온다


    def attack(self):
        pass

    def _attack_motion(self):
        #앞을 보고 공격한다."
        pass

    def take_damage(self, damage: "int", origin: "Vector2 | None" = None):
        #지정된 양만큼의 데미지를 입는다."
        self.hp -= damage
