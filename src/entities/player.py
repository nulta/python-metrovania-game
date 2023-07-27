import pygame
from .entity import *

class Player(Entity):
    def __init__(self, gender,speed):
        super().__init__()
        self._hp = 200
        self._gender = gender
        self._move_speed = speed
        self._item = None

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
        # 입력 처리, 이동 처리, 기타 등등...
        pass

    def draw(self):
        super().draw()

        # 가져와야 할 이미지의 이름을 조립한다
        image_path = ASSET_PATH + "/player"
        if self._gender == GENDER_MALE:
            image_path += "/male"
        else:
            image_path += "/female"

        image_path += "/" + (self._item or "idle")
        image_path += ".png"

        # 조립한 이미지 이름대로, 불러온다
        pygame.image.load(image_path)

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
