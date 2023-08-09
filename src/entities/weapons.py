from .entity import *
from .player import *
from .enemy import *
from pygame.math import Vector2
from constants import *

class Weapon(Entity):
    def use(self):
        pass

#-----------------------------------------------------------

class gun(Weapon):
    def attack(self):
        self._grenade_speed = 50

class FB85(Weapon): #칠겹살용 토치
    def __init__(self,damage,velocity =Vector2(0,0)):
        self._damage = damage
        self._velocity = velocity
        #불이 나온다

class BB02(Weapon):#나이키에어
    def __init__(self,damage):
        self._damage=damage

    def position(self):
        Player.position.y += Player.image_height/2
        #신발에서 바람이 나온다 높이가 높아짐?
        #enemy로부터 2칸 안에 있으면 공격

class SN92(Weapon): #아디다su
    def __init__(self,add_speed):
        Player._move_speed += add_speed
        #캐릭터 속도를 높인다.

class SB87(Weapon): #대청단 감자주머니
    def __init__(self):
        super().__init__()
        self._grenade_speed = 50

class VP33(Weapon): #지구온난화의 주범
    def attack(self):
        Poison._velocity += 50

    def gass(self,speed_reduction):
        for event in pygame.event .get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    Enemy._move_speed -= speed_reduction
                    start_ticks= pygame.time.get_ticks()
                    elapsed_time = (pygame.time.get_ticks()- start_ticks)/1000
                    if 3 - elapsed_time <=0:
                        Enemy._move_speed += speed_reduction
        #독을 발포한다
        #가스를 살포한다(enemy의 속도가 늘어진다)

class KS64(Weapon): #로이드가 입던 옷
    def position(self,damage):
        Player.position = Boss.position
        if Player.position == Boss.position:
            Boss.take_damage(damage)
        #boss의 위치로 순간이동 한다
        #접촉하면 몬스터의 체력이 깍인다

class Bullet(Entity):
    def __init__(self, damage,velocity =Vector2(0,0)):
        super().__init__()
        self._damage = damage
        self._velocity = velocity

class Poison(Entity):
    def __init__(self, damage,velocity = Vector2(0,0)):
        super().__init__()
        self._damage = damage
        self._velocity = velocity

class Grenade(Entity):
    def __init__(self, damage, velocity = Vector2(0, 0)):
        super().__init__()
        self._damage = damage
        self._velocity = velocity

    def update(self):
        super().update()

    def _explode(self,damage):
        width =self.position.x - Player.position.x
        height = self.position.y -Player.position.y
        if self.position == Player.position:
            Player.take_damage(damage) #2차 피해

        elif (width**2- height**2)**(1/2) < Weapon.image_height:
            Player.position.x -= width


        # 폭발 이펙트를 재생한다.
        # 근처에 플레이어가 있는지 확인.
        #   있다면, 데미지와 넉백을 준다.
        # 자기 자신을 삭제한다.