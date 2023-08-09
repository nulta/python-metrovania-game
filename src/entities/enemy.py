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
        pass

    def surface(self,enemy_name):
        super().surface()
        # 적의 모습을 화면에 그린다.
        image_path = RESOURCE_PATH + "/enemy/"
        image_path += enemy_name
        image_path += ".png"
        # 조립한 이미지 이름대로, 불러온다
        self.image=pygame.image.load(image_path)
        self.image_size = self.image.get_rect().size
        self.image_width = self.image_size[0] #아이템 가로크기
        self.image_height = self.image_size[1]


    def _attack(self):
        #앞을 보고 공격한다."
        pass

    def take_damage(self, damage):
        #지정된 양만큼의 데미지를 입는다."
        self.hp -= damage

#-------------------------------------------------------
class FB_88(Enemy):
    def attack(self):
        #불을 발사한다"
        width =self.position.x - Player.position.x
        if width>0:
            FB85._velocity += -50
        elif width<0:
            FB85._velocity += 50
            
    def take_damage(self, damage):
        #지정된 양만큼의 데미지를 입는다.
        self.hp -= damage

class BT_02(Enemy):
    def attack(self,damage):
        width =self.position.x - Player.position.x
        height = self.position.y -Player.position.y
        if (width**2- height**2)**(1/2) < self.image_height*(3/2):
            Player.position.x -= width
            Player.take_damage(damage)
        #상대를 바람으로 공격한다"
        #상대가 바람에 의해 뒤로 이동한다"

    def take_damage(self, damage):
        #지정된 양만큼의 데미지를 입는다.
        self.hp -= damage
        
class SN_91(Enemy):
    def __init__(self):
        super().__init__()
        self._move_speed = 20
        #속도가 빠르다"
        
    def attack(self,damage):
        width =self.position.x - Player.position.x
        if abs(width) < self.image_height:
            Player.take_damage(damage)
            
class SB_87(Enemy):
    def attack(self):
        width =self.position.x - Player.position.x
        if width>0:
            Grenade._velocity = -50
        elif width<0:
            Grenade._velocity = 50
    

class VP_33(Enemy):
    def attack(self,damage):
        begin = time.time()
        if time.time()-begin <= 2:
            Player._move_speed -= 2
            Player.take_damage(damage)
        elif time.time()-begin > 2:
            Player._move_speed +=2

        #""전방향""으로 독가스를 살포한다
        
class KS_64(Enemy):
    def move_position(self,damage):
        self.position = Player.position
        if self.position == Player.position:
            Player.take_damage(damage)
        #player의 위치로 순간이동 한다
        #접촉하면 플레이어의 체력이 깍인다

B_F = BOSS_MASS*BOSS_VELOCITY**2/2
        
class Boss(Enemy):
    def __init__(self):
        super().__init__()
        self.hp = 200
        self._move_speed = 15
        #체력과 속도가 늘어남
        self.isJump = 0
        self.v = BOSS_VELOCITY
        self.m = BOSS_MASS

    def jump(self,damage):
        if self.isJump >0:
            if self.isJump ==2:
                self.v = BOSS_VELOCITY
            if self.v >0:
                F = 0.5*self.m*(self.v*self.v)
            else:
                F = 0.5*self.m*(self.v*self.v)*(-1)
            self.position.y -= round(F)
            self.v -= 1
            if self.image.bottom > GAME_WINDOW_SIZE[1]:
                self.image.bottom = GAME_WINDOW_SIZE[1]
                self.isJump =0
                self.v = BOSS_VELOCITY

        if self.position == Player.position:
            Player.take_damage(damage)


    def avoid(self):
        #몹의 공격을 피한다
        pass