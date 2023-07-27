from .entity import *

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
        
    def update(self):
        super().__init()
        #점프를 추가해야한다
        
    def avoid(self):
        #몹의 공격을 피한다
        pass
        