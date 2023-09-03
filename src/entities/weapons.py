from .entity import *
from .player import *
from .enemy import *
from pygame.math import Vector2
from constants import *
import game_globals
from resource_loader import ResourceLoader
from input_manager import InputManager
from constants import *
from audio import Audio
from fonts import Fonts
import util

class Weapon(Entity):
    def update(self):
        pass

    def use(self):
        pass

#-----------------------------------------------------------

class gun(Weapon):
    def attack(self):
        from entity_manager import EntityManager
        bullet = EntityManager.get_bullet()
        if not bullet: return                # None일 경우 return
        enemy = EntityManager.get_enemy()
        if not enemy: return   
        bullet._velocity += 50
        if bullet.position == enemy.position:
            enemy.take_damage(bullet._damage)

class FB85(Entity): #칠겹살용 토치 ---(의 불..)
    def attack(self):
        from entity_manager import EntityManager
        fire = EntityManager.get_fire()
        enemy = EntityManager.get_enemy()
        if not enemy: return  
        if not fire: return                # None일 경우 return
        fire._velocity += 50
        if fire.position == enemy.position:
            enemy.take_damage(fire._damage)

class BB02(Weapon):#나이키에어
    def __init__(self,damage):
        self._damage=damage

    def position_y(self):
        from entity_manager import EntityManager
        player = EntityManager.get_player()
        if not player: return                # None일 경우 return
        player.position.y += 15
        #신발에서 바람이 나온다 높이가 높아짐?
        #enemy로부터 2칸 안에 있으면 공격

class SN92(Weapon): #아디다su
    def __init__(self,add_speed):
        from entity_manager import EntityManager
        player = EntityManager.get_player()
        if not player: return                # None일 경우 return
        player._move_speed += add_speed
        #캐릭터 속도를 높인다.

class SB87(Weapon): #대청단 감자주머니
    def __init__(self):
        from entity_manager import EntityManager
        grenade = EntityManager.get_grenade_player()
        if not grenade: return               # None일 경우 return
        grenade._velocity += 50

class VP33_poison(Weapon): #지구온난화의 주범
    def attack(self):
        from entity_manager import EntityManager
        poison = EntityManager.get_poison()  # Poison 또는 None
        if not poison: return                # None일 경우 return
        poison._velocity += 50
class VP33_gas(Weapon):
    def gas(self,speed_reduction):
        from entity_manager import EntityManager
        enemy = EntityManager.get_enemy()  # Enemy 또는 None
        if not enemy: return                # None일 경우 return
        enemy._move_speed -= speed_reduction
        start_ticks= pygame.time.get_ticks()
        elapsed_time = (pygame.time.get_ticks()- start_ticks)/1000
        if 3 - elapsed_time <=0:
            enemy._move_speed += speed_reduction
        #독을 발포한다
        #가스를 살포한다(enemy의 속도가 늘어진다)

class KS64(Weapon): #로이드가 입던 옷
    def position_x(self,damage):
        from entity_manager import EntityManager
        enemy = EntityManager.get_enemy()  # Enemy 또는 None
        if not enemy: return                # None일 경우 return
        Player.position = enemy.position
        if Player.position == enemy.position:
            enemy.take_damage(damage)
        #enemy의 위치로 순간이동 한다
        #접촉하면 몬스터의 체력이 깍인다

class Bullet(Entity):
    def __init__(self, damage,velocity):
        super().__init__()
        self._damage = damage
        self._velocity = velocity

class Fire(Entity):
    def __init__(self, damage,velocity):
        super().__init__()
        self._damage = damage
        self._velocity = velocity

class Poison(Entity):
    def __init__(self, damage,velocity):
        super().__init__()
        self._damage = damage
        self._velocity = velocity

class Grenade_enemy(Entity): #enemy가 사용하는(넉백떄문에 따로 만들었슴다..!)
    def __init__(self, damage, velocity):
        super().__init__()
        self._damage = damage
        self._velocity = velocity

    def update(self):
        super().update()

    def _explode(self,damage):
        from entity_manager import EntityManager
        player = EntityManager.get_player()  # Player 또는 None
        if not player: return                # None일 경우 return

        width =self.position.x - player.position.x
        height = self.position.y -player.position.y
        if self.position == player.position:
            player.take_damage(damage) #2차 피해

        elif (width**2- height**2)**(1/2) < 120 :
            player.position.x -= width
        # 폭발 이펙트를 재생한다.
        # 근처에 플레이어가 있는지 확인.
        #   있다면, 데미지와 넉백을 준다.
        # 자기 자신을 삭제한다.


class Grenade_player(Entity): #player가 사용하는(넉백떄문에 따로 만들었슴다..!)
    def __init__(self, damage, velocity):
        super().__init__()
        self._damage = damage
        self._velocity = velocity

    def update(self):
        super().update()

    def _explode(self,damage):
        from entity_manager import EntityManager
        enemy = EntityManager.get_enemy()  # Player 또는 None
        if not enemy: return                # None일 경우 return

        width =self.position.x - enemy.position.x
        height = self.position.y -enemy.position.y
        if self.position == enemy.position:
            enemy.take_damage(damage) #2차 피해

        elif (width**2- height**2)**(1/2) < 120 :
            enemy.position.x -= width
        # 폭발 이펙트를 재생한다.
        # 근처에 플레이어가 있는지 확인.
        #   있다면, 데미지와 넉백을 준다.
        # 자기 자신을 삭제한다.