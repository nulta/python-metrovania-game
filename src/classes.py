from pygame.math import Vector2

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


GENDER_MALE   = 0
GENDER_FEMALE = 1

class Player(Entity):
    def __init__(self, gender=GENDER_FEMALE):
        super().__init__()
        self._hp = 100
        self._gender = gender
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
        # 입력 처리, 이동 처리, 기타 등등...
        pass
    
    def draw(self):
        super().draw()
        # 플레이어의 모습을 화면에 그린다.
        pass

    
    def _shoot(self):
        pass
    
    def _move(self):
        pass


    def take_damage(self, damage):
        #지정된 양만큼의 데미지를 입는다.
        self.hp -= damage
        
        
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


class FB_85(Enemy):    
    def attack(self):
        #불을 발사한다"
        pass


class BT_02(Enemy):
    def attack(self):
        pass
        #상대를 바람으로 공격한다"
        #상대가 바람에 의해 뒤로 이동한다"


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
        
    
class Item(Entity):
    def use(self):
        pass

class gun(Item):
    def attack():
        self._grenade_speed = 50

class FB85(Item):
    def attack():
        pass

class Bullet(Entity):
    def __init__(self, damage):
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
