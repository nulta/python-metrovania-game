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
        from entity_manager import EntityManager
        player = EntityManager.get_player()
        if not player: return  
        if self.position.x <= player.position.x:
            self.position.x += 1
        elif self. position.x>= player.position.x:
            self.position.x -=1

    def surface(self,enemy_name):
        super().surface()
        # 적의 모습을 화면에 그린다.
        image_path = RESOURCE_PATH + "/enemy/"
        image_path += enemy_name
        image_path += ".png"
        # 조립한 이미지 이름대로, 불러온다



    def _attack(self):
        #앞을 보고 공격한다."
        pass

    def take_damage(self, damage):
        #지정된 양만큼의 데미지를 입는다."
        self.hp -= damage

#-------------------------------------------------------
class FB_88(Enemy):
    def attack(self):
        from entity_manager import EntityManager
        player = EntityManager.get_player()
        if not player: return                # None일 경우 return
        fire = EntityManager.get_fire()
        if not fire: return   

        #불을 발사한다"
        width =self.position.x - player.position.x
        if width>0:
            fire._velocity += -50
        elif width<0:
            fire._velocity += 50
            
    def take_damage(self, damage):
        #지정된 양만큼의 데미지를 입는다.
        self.hp -= damage

class BT_02(Enemy):
    def attack(self,damage):
        from entity_manager import EntityManager
        player = EntityManager.get_player()  # Player 또는 None
        if not player: return                # None일 경우 return
        # 이제부터, player 변수는 None일 수가 없음
        width =self.position.x - player.position.x
        height = self.position.y -player.position.y
        if (width**2- height**2)**(1/2) < 120:
            player.position.x -= width
            player.take_damage(damage)
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
        from entity_manager import EntityManager
        player = EntityManager.get_player()  # Player 또는 None
        if not player: return                # None일 경우 return
        width =self.position.x - player.position.x
        if abs(width) < 30:
            player.take_damage(damage)
            
class SB_87(Enemy):
    def attack(self):
        from entity_manager import EntityManager
        player = EntityManager.get_player()  # Player 또는 None
        if not player: return                # None일 경우 return
        grenade = EntityManager.get_grenade_enemy()  # Grenade 또는 None
        if not grenade: return                # None일 경우 return
        width =self.position.x - player.position.x
        if width>0:
            grenade._velocity = -50
        elif width<0:
            grenade._velocity = 50
    

class VP_33(Enemy):
    def attack(self,damage):
        from entity_manager import EntityManager
        player = EntityManager.get_player()  # Player 또는 None
        if not player: return                # None일 경우 return
        begin = time.time()
        if time.time()-begin <= 2:
            player._move_speed -= 2
            player.take_damage(damage)
        elif time.time()-begin > 2:
            player._move_speed +=2

        #""전방향""으로 독가스를 살포한다
        
class KS_64(Enemy):
    def move_position(self,damage):
        from entity_manager import EntityManager
        player = EntityManager.get_player()
        if not player: return                # None일 경우 return
        self.position = player.position
        if self.position == Player.position:
            player.take_damage(damage)
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
            self._pivot = Vector2(15, 30)
            if self.isJump ==2:
                self.v = BOSS_VELOCITY
            if self.v >0:
                F = 0.5*self.m*(self.v*self.v)
            else:
                F = 0.5*self.m*(self.v*self.v)*(-1)
            self.position.y -= round(F)
            self.v -= 1
            if self.position.y > GAME_WINDOW_SIZE[1]:
                self.position.y = GAME_WINDOW_SIZE[1]
                self.isJump =0
                self.v = BOSS_VELOCITY
        self._pivot = Vector2(15, 15)

        if self.position == Player.position:
            from entity_manager import EntityManager
            player = EntityManager.get_player()  # Player 또는 None
            if not player: return                # None일 경우 return
            player.take_damage(damage)


    def avoid(self):
        #몹의 공격을 피한다
        pass