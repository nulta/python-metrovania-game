import pygame
import game_globals
from resource_loader import ResourceLoader
from .scene import Scene
from input_manager import InputManager
from constants import *
from audio import Audio
from fonts import Fonts
import math
import util
from scene_manager import *
from .game_scene import *
from typing import *


class ChooseScene(Scene):
    """Player 선택 창이다"""

    music_name = ""
    character_image = ""
    player_name = ""
    color = (128,128,128)
    select_color = (255, 255, 255)
    def __init__(self):
        super().__init__()

        # 음악을 재생한다.
        if self.music_name:
            music = f"sounds/music/{self.music_name}.ogg"
            music_path = ResourceLoader.get_resource_path(music)
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(-1)

        self._focus_index = 0

    def update(self):
        # 메뉴 이동 처리 (키보드)
        if InputManager.pressed(ACTION_LEFT):
            Audio.common.select()
            self._focus_index = 1
        elif InputManager.pressed(ACTION_RIGHT):
            Audio.common.select()
            self._focus_index = 2

        # 메뉴 입력 처리 (키보드)
        if InputManager.pressed(ACTION_CONFIRM):
            Audio.common.confirm()
            self.press_charcter(self._focus_index)

    def draw_button(self,surface: pygame.Surface):
        if self._focus_index == 1:
            button1_color= self.select_color
            button2_color = self.color
        elif self._focus_index == 2:
            button1_color= self.color
            button2_color = self.select_color
        else:
            button1_color= self.color
            button2_color= self.color

        pygame.draw.rect(surface, button1_color,[110,150,255,300])
        pygame.draw.rect(surface, button2_color,[500,150,255,300])            


    def draw(self, surface: "Surface"):
        self.draw_background(surface)
        self.draw_title(surface)
        self.draw_button(surface)
        self.draw_character(surface)
        self.draw_info(surface)

    def draw_background(self, surface: pygame.Surface):
        # 배경 그리기
        scence_path = ResourceLoader.load_image("background/intro.png")
        surface.blit(scence_path, (0, 0))

    def draw_character(self, surface: pygame.Surface):
        # 사람 그리기
        male_path = ResourceLoader.load_image_2x("player/male/idle_1.png")
        female_path = ResourceLoader.load_image_2x("player/female/idle_1.png")

        surface.blit(male_path, (140,200))
        surface.blit(female_path, (530, 200))


    def press_charcter(self, button_index):
        if button_index == 1:
            #남자
            game_globals.player_gender=GENDER_MALE
            from scene_manager import SceneManager
            from .story_scene import StorySceneIntro
            SceneManager.clear_scene()
            SceneManager.push_scene(StorySceneIntro())
        elif button_index == 2:
            # 여자
            game_globals.player_gender=GENDER_FEMALE
            from scene_manager import SceneManager
            from .story_scene import StorySceneIntro
            SceneManager.clear_scene()
            SceneManager.push_scene(StorySceneIntro())

    def draw_title(self,surface: pygame.Surface):
        # 부제..? 그리기
        Fonts.get("bold").render_to(
            surface,
            (330, 60),
            "캐릭터 선택",
            fgcolor=(255, 255, 255),
            size=45,
        )
    def draw_info(self,surface: pygame.Surface):
        # 안내문 그리기
        Fonts.get("bold").render_to(
            surface,
            (350, 555),
            "ENTER를 눌러 선택합니다",
            fgcolor=(255, 255, 255),
            size=15,
        )

    def on_destroy(self):
        pygame.mixer.music.unload()
