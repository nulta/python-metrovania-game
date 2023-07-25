from pygame.math import Vector2
from constants import *
import pygame
import os

class Entity():
    def __init__(self):
        self._position = Vector2(0, 0)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value


    def think(self):
        pass

    def draw(self):
        pass

########################################################


class Player(Entity):
    def __init__(self, gender,speed):
        super().__init__()
        self._hp = 200
        self._gender = gender
        self._move_speed = speed

    @property
    def hp(self):
        return self._hp
    
    @hp.setter
    def hp(self, value):
        if value < 0:
            value = 0
        self._hp = value
        
    
    def think(self):
        super().think()
        # 입력 처리, 이동 처리, 기타 등등...
        pass
    
    def draw(self,gender,item): #아이템이 없으면 "item == 0", # male == 0, female == 1
        super().draw()
        if gender == 0 and item == 0:
            pygame.image.load(ASSET_PATH + "sprites/player(male,game).png")
        elif gender ==1 and item == 0:
            pygame.image.load(ASSET_PATH + "sprites/player(female,game).png")
        elif gender == 0 and item == "gun": #튜토리얼
            pygame.image.load(ASSET_PATH + "sprites/player(with gun).png")
        elif gender == 1 and item == "gun":
            pass
        elif gender == 0 and item == "FB85": #1라운드 끝나면 주는 것, 칠겹살용 토치
            pass
        elif gender == 1 and item == "FB85":
            pass
        elif gender == 0 and item == "BB02": #2라운드 끝나명 주는 것, 나이키 에어
            pass
        elif gender == 1 and item == "BB02": 
            pass
        elif gender == 0 and item == "SN92": #3라운드 끝나명 주는 것, 아디다SU
            pass
        elif gender == 1 and item == "SN92":
            pass
        elif gender == 0 and item == "SB87": #4라운드 끝나명 주는 것, 대청단감자주머니
            pass
        elif gender == 1 and item == "SB87":
            pass
        elif gender == 0 and item == "VP33": #5라운드 끝나명 주는 것, 지구온난화의 주범
            pass
        elif gender == 1 and item == "VP33":
            pass
        elif gender == 0 and item == "KS64": #6라운드 끝나명 주는 것, 로이드가 입던옷(순간이동)
            pass
        elif gender == 1 and item == "KS64":
            pass

    def _shoot(self):
        pass
    
    def _move(self,speed):
        dt=pygame.time.Clock.tick(30)
        
        for event in pygame.event .get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w: #캐릭터 점프
                    pass
                if event.key == pygame.K_d: #캐릭터 오른쪽으로
                    player_to_x += speed
                if event.key == pygame.K_a: #캐릭터 왼쪽으로
                    player_to_x -= speed

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    player_to_x = 0
                
        player_x_pos += player_to_x*dt
 
    def take_damage(self, damage):
        #지정된 양만큼의 데미지를 입는다.
        self.hp -= damage
         
##################################################################

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

    def think(self):
        super().think()
        # AI 처리, 이동 처리, 기타 등등...
        pass

    def draw(self):
        super().draw()
        # 적의 모습을 화면에 그린다.
        pass


    def _attack(self):
        #앞을 보고 공격한다."
        pass

    def take_damage(self, damage):
        #지정된 양만큼의 데미지를 입는다."
        self.hp -= damage

#-------------------------------------------------------
class FB_85(Enemy):    
    def attack(self):
        #불을 발사한다"
        pass
    def take_damage(self, damage):
        #지정된 양만큼의 데미지를 입는다.
        self.hp -= damage
    def draw(self):
        super().draw()


class BT_02(Enemy):
    def attack(self):
        pass
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
        
    def attack(self):
        pass
        #공격한다"


class SB_87(Enemy):
    def __init__(self):
        super().__init__()
        self._grenade_speed = 50  # 수류탄 던지는 속도

class VP_33(Enemy):
    def attack(self):
        super().attack()
        #""전방향""으로 독가스를 살포한다
        pass
        
        
class KS_64(Enemy):
    def position(self):
        pass
        #player의 위치로 순간이동 한다
        #접촉하면 플레이어의 체력이 깍인다
        
class Boss(Enemy):
    def __init__(self):
        super().__init__()
        self.hp = 200
        self._move_speed = 15
        #체력과 속도가 늘어남
        
    def think(self):
        super().__init()
        #점프를 추가해야한다
        
    def avoid(self):
        #몹의 공격을 피한다
        pass
        
#######################################################################333

class Item(Entity):
    def use(self):
        pass
#-----------------------------------------------------------
class gun(Item):
    def attack(self):
        self._grenade_speed = 50

class FB85(Item): #칠겹살용 토치
    def attack(self):
        pass
        #불이 나온다

class BB02(Item):#나이키에어
    def position(self):
        pass
        #신발에서 바람이 나온다 높이가 높아짐?

class SN92(Item): #아디다su
    def move(self):
        pass
        #캐릭터 속도를 높인다.

class SB87(Item): #대청단 감자주머니
    def __init__(self):
        super().__init__()
        self._grenade_speed = 50

class VP33(Item): #지구온난화의 주범
    def attack(self):
        #독을 발포한다
        #가스를 살포한다(enemy의 속도가 늘어진다)
        pass
class KS64(Item): #로이드가 입던 옷
    def position(self):
        pass
        #boss의 위치로 순간이동 한다
        #접촉하면 몬스터의 체력이 깍인다

class Bullet(Entity):
    def __init__(self, damage,velocity =Vector2(0,0)):
        super().__init__()
        self._damage = damage
        self._velocity = velocity


class Grenade(Entity):
    def __init__(self, damage, velocity = Vector2(0, 0)):
        super().__init__()
        self._damage = damage
        self._velocity = velocity


    def think(self):
        super().think()


    def _explode(self):
        # 폭발 이펙트를 재생한다.
        # 근처에 플레이어가 있는지 확인.
        #    있다면, 데미지와 넉백을 준다.
        # 자기 자신을 삭제한다.
        pass
