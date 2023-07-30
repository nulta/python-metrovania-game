from .entity import *

class Weapon(Entity):
    def use(self):
        pass

#-----------------------------------------------------------

class gun(Weapon):
    def attack(self):
        self._grenade_speed = 50

class FB85(Weapon): #칠겹살용 토치
    def attack(self):
        pass
        #불이 나온다

class BB02(Weapon):#나이키에어
    def position(self):
        pass
        #신발에서 바람이 나온다 높이가 높아짐?

class SN92(Weapon): #아디다su
    def move(self):
        pass
        #캐릭터 속도를 높인다.

class SB87(Weapon): #대청단 감자주머니
    def __init__(self):
        super().__init__()
        self._grenade_speed = 50

class VP33(Weapon): #지구온난화의 주범
    def attack(self):
        #독을 발포한다
        #가스를 살포한다(enemy의 속도가 늘어진다)
        pass
class KS64(Weapon): #로이드가 입던 옷
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


    def _explode(self,damage):
        width =self.position.x - Player.position.x
        height = self.position.y -Player.position.y
        if self.position == Player.position:
            Player.take_damage(damage) #2차 피해

        elif (width**2- height**2)**(1/2) < Item.image_height:
            Player.position.x -= width


        # 폭발 이펙트를 재생한다.
        # 근처에 플레이어가 있는지 확인.
        #   있다면, 데미지와 넉백을 준다.
        # 자기 자신을 삭제한다.