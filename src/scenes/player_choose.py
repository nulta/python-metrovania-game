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

    character_image = ""
    player_name = ""
    color = (128,128,128)
    select_color = (255, 255, 255)
    def __init__(self):
        super().__init__()
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

    def draw(self, surface: "Surface"):
        self.draw_background(surface)
        self.draw_storyboard(surface)
        # self.draw_title(surface)
        self.draw_arrow(surface)
        self.draw_character(surface)

        scence_path = ResourceLoader.load_image("background/intro/frame.png")
        surface.blit(scence_path, (0, 0))

        self.draw_info(surface)

    def draw_arrow(self,surface: pygame.Surface):
        if self._focus_index == 0:
            return
        elif self._focus_index == 1:
           self.position_x= 320
        else:
            self.position_x= 590

        storyboard_path = ResourceLoader.load_image_2x(f"background/arrow.png")
        surface.blit(storyboard_path, (self.position_x, 50))
           

    def draw_storyboard(self, surface: pygame.Surface):
        # 사람 그리기
        font_size = 18
        color = (0, 0, 0)
        if self._focus_index == 0:
            text = "캐릭터를 선택하세요"
            self.position_x = 110
            storyboard_path = ResourceLoader.load_image(f"story_board/blank.png")

        elif self._focus_index == 1:
            text = "A"
            self.position_x = 330
            storyboard_path = ResourceLoader.load_image(f"story_board/male/player.png")

        else:
            text = "B"
            self.position_x = 330
            storyboard_path = ResourceLoader.load_image(f"story_board/female/player.png")

        surface.blit(storyboard_path, (0, 0))
        Fonts.get("default").render_to(
        surface,
        (self.position_x, 400),
        text,
        fgcolor=color,
        size=font_size,
        )

    def draw_background(self, surface: pygame.Surface):
        # 배경 그리기
        cloud_offset = math.sin(self.scene_time / 3) * 30

        surface.blit(ResourceLoader.load_image("background/intro/sky.png"), (0, 0))
        surface.blit(ResourceLoader.load_image("background/intro/stardust.png"), (0, 0))
        surface.blit(ResourceLoader.load_image("background/intro/cloud.png"), (0, cloud_offset))

    def draw_character(self, surface: pygame.Surface):
        # 사람 그리기
        male_path = ResourceLoader.load_image_5x("player/male/choose.png")
        female_path = ResourceLoader.load_image_5x("player/female/choose.png")

        surface.blit(male_path, (280,150))
        surface.blit(female_path, (550, 150))


    def press_charcter(self, button_index):
        if button_index == 1:
            #남자
            game_globals.player_gender=GENDER_MALE
        elif button_index == 2:
            # 여자
            game_globals.player_gender=GENDER_FEMALE
        else:
            from scene_manager import SceneManager
            from .player_choose import ChooseScene
            SceneManager.clear_scene()
            SceneManager.push_scene(ChooseScene())
        from scene_manager import SceneManager
        from .story_scene import StorySceneIntro
        SceneManager.clear_scene()
        SceneManager.push_scene(StorySceneIntro())

    def draw_info(self,surface: pygame.Surface):
        # 안내문 그리기
        Fonts.get("bold").render_to(
            surface,
            (350, 555),
            "ENTER or Space를 눌러 선택합니다",
            fgcolor=(255, 255, 255),
            size=15,
        )

    def on_destroy(self):
        # Audio.music_set("")
        pass
