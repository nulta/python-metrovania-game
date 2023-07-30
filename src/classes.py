from pygame.math import Vector2
from constants import *
import pygame
import time

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

F = PLAYER_MASS*PLAYER_VELOCITY*PLAYER_VELOCITY/2

class Player(Entity):
    def __init__(self, gender,speed):
        super().__init__()
        self._hp = 200
        self._gender = gender
        self._move_speed = speed
        self._item = None
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
        
    
    def think(self):
        super().think()
        # 입력 처리, 이동 처리, 기타 등등...
        pass
    
    def draw(self):
        super().draw()

        # 가져와야 할 이미지의 이름을 조립한다
        image_path = RESOURCE_PATH + "/player"
        if self._gender == GENDER_MALE:
            image_path += "/male"
        else:
            image_path += "/female"

        image_path += "/" + (self._item or "idle")
        image_path += ".png"

        # 조립한 이미지 이름대로, 불러온다
        self.image=pygame.image.load(image_path)
        self.image=self.image.get_rect()
        self.image_size = self.image.get_rect().size
        self.image_width = self.image_size[0] 
        self.image_height = self.image_size[1] 

    def _shoot(self):
        pass
    
    def _move(self,speed):
        player_x_pos=self.position.x
        player_to_x = 0
        
        for event in pygame.event .get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d: #캐릭터 오른쪽으로
                    player_to_x += speed
                if event.key == pygame.K_a: #캐릭터 왼쪽으로
                    player_to_x -= speed

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    player_to_x = 0

        dt=pygame.time.Clock().tick(30)        
        player_x_pos += player_to_x*dt

    def jump(self):
        if self.isJump >0:
            if self.isJump ==2:
                self.v = PLAYER_VELOCITY
            if self.v >0:
                F = 0.5*self.m*(self.v*self.v)
            else:
                F = 0.5*self.m*(self.v*self.v)*(-1)
            self.position.y -= round(F)
            self.v -= 1
            if self.image.bottom > GAME_WINDOW_SIZE[1]:
                self.image.bottom = GAME_WINDOW_SIZE[1]
                self.isJump =0
                self.v = PLAYER_VELOCITY




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

    def draw(self,enemy_name):
        super().draw()
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
class FB_85(Enemy):    
    def attack(self):
        #불을 발사한다"
        width =self.position.x - Player.position.x
        if width>0:
            FB85._velocity = -50
        elif width<0:
            FB85._velocity = 50
            
            
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
    def think(self):
        super().think()
        
    def avoid(self):
        #몹의 공격을 피한다
        pass
        
#######################################################################333

class Item(Entity):
    def use(self):
        pass

    def draw(self,Item_name):
        super().draw()
        # 적의 모습을 화면에 그린다.
        image_path = RESOURCE_PATH + "/Item/"
        image_path += Item_name
        image_path += ".png"
        # 조립한 이미지 이름대로, 불러온다
        self.image=pygame.image.load(image_path)
        self.image_size = self.image.get_rect().size
        self.image_width = self.image_size[0] #아이템 가로크기
        self.image_height = self.image_size[1]
#-----------------------------------------------------------
class gun(Item):
    def attack(self):
        Bullet._velocity += 50

class FB85(Item): #칠겹살용 토치
    def __init__(self,damage,velocity =Vector2(0,0)):
        self._damage = damage
        self._velocity = velocity
        #불이 나온다

class BB02(Item):#나이키에어
    def __init__(self,damage):
        self._damage=damage

    def position(self):
        Player.position.y += Player.image_height/2
        #신발에서 바람이 나온다 높이가 높아짐?
        #enemy로부터 2칸 안에 있으면 공격

class SN92(Item): #아디다su
    def __init__(self,add_speed):
        Player._move_speed += add_speed
        #캐릭터 속도를 높인다.

class SB87(Item): #대청단 감자주머니
    def __init__(self):
        super().__init__()
        Grenade._velocity += 50

class VP33(Item): #지구온난화의 주범
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
        

class KS64(Item): #로이드가 입던 옷
    def position(self,damage):
        Player.position = Boss.position
        if Player.position == Boss.position:
            Boss.take_damage(damage)
        #boss의 위치로 순간이동 한다
        #접촉하면 몬스터의 체력이 깍인다

class Box(Item):
    def use(self):
        ##....... 이거 어케함까..?
        #enemy가 캐릭터를 인식하지 못한다
        pass

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

