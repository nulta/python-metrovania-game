import pygame
from .entity import *

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