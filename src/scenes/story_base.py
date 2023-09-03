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

class StoryScene(Scene):
    """Story은 이야기가 나올 때 기본적인 틀이다."""

    _button_texts = ["건너뛰기(ESC)", "▽"]
    music_name = ""
    line = []
    info_texts = ["ENTER 키를 누르면 다음 대사로 넘어간다",
                  "ESC 키를 누르면 이 장면이 스킵된다"]
    background_image = ""
    character_image = ""
    next_scene: Scene = None  # type: ignore
    def __init__(self):
        super().__init__()
        self.i=0
        # 음악을 재생한다.
        if self.music_name:
            music = f"sounds/music/{self.music_name}.ogg"
            music_path = ResourceLoader.get_resource_path(music)
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(-1)


    def update(self):
        # 메뉴 이동 처리 (키보드)
        #건너뛰기
        from scene_manager import SceneManager
        if InputManager.pressed(ACTION_CANCEL):
            Audio.common.select()
            SceneManager.clear_scene()
            SceneManager.push_scene(self.next_scene)
        #다음대사
        elif InputManager.pressed(ACTION_CONFIRM):
            Audio.common.select()
            self.i +=1
            if len(self.line)== self.i:
                SceneManager.clear_scene()
                SceneManager.push_scene(self.next_scene)

    def draw(self, surface: "Surface"):
        self.draw_background(surface, self.background_image)
        self.draw_character(surface,self.character_image)
        self.draw_info(surface)
        self.draw_skip(surface)
        self.draw_stroyboard(surface)
        self.draw_line(surface)
        self.draw_next(surface)

    def draw_background(self, surface: pygame.Surface, scence):
        # 배경 그리기
        if True:
            scence_path = ResourceLoader.load_image_2x(f"sprites/background/{scence}.png")
            surface.blit(scence_path, (0, 0))
    def draw_character(self, surface: pygame.Surface,character):
        if not character: return

        # 사람 그리기
        character_path = ResourceLoader.load_image_2x(f"sprites/story_character/{character}.png")
        surface.blit(character_path, (550, 200))

        #스트리보드 그리기
    def draw_stroyboard(self,surface: pygame.Surface):
        storyboard_path = ResourceLoader.load_image("sprites/background/storyboard.png")
        surface.blit(storyboard_path, (0, 0))  
    def draw_skip(self,surface: pygame.Surface):
        # 건너뛰기 그리기
        pygame.draw.rect(surface,(0,0,0),[680,30,140,40],0)

        text = self._button_texts[0]
        font_size = 20
        color = (255, 255, 255)

        Fonts.get("bold").render_to(
            surface,
            (690, 40),
            text,
            fgcolor=color,
            size=font_size,
            )

    def draw_next(self,surface: pygame.Surface):
        # 다음대사 버튼 그리기
        text = self._button_texts[1]
        font_size = 15
        color = (255, 255, 255)
        Fonts.get("bold").render_to(
            surface,
            (740, 400),
            text,
            fgcolor=color,
            size=font_size,
            )
    def draw_line(self,surface: pygame.Surface):
        # 대사 그리기
        text = self.line[self.i]
        font_size = 25
        color = (255, 255, 255)

        Fonts.get("default").render_to(
            surface,
            (70, 420),
            text,
            fgcolor=color,
            size=font_size,
        )


    def draw_info(self,surface: pygame.Surface):
        # 안내문 그리기
        for idx, text in enumerate(self.info_texts):
            font_size = 15
            y_offset = idx * (font_size + 3) + (math.sin(self.scene_time * 2.5 + idx/2) * 5)
            color = (0, 220, 255)
            Fonts.get("bold").render_to(
                surface,
                (300, 555 + y_offset),
                text,
                fgcolor=color,
                size=font_size,
            )
    def on_destroy(self):
        pygame.mixer.music.unload()


class StorySceneIntro(StoryScene):
    line = ["ㅡ",
            "러ㅏㄹㄹ",
            "아ㅓ라ㅓ아러ㅏㅇ"
            ]
    
    _button_texts = ["건너뛰기(ESC)", "▽"]
    music_name = ""
    info_texts = ["ENTER 키를 누르면 다음 대사로 넘어간다",
                  "ESC 키를 누르면 이 장면이 스킵된다"]
    background_image = "intro"
    character_image = "fanboy"
    next_scene: Scene = GameScene(None)  # type: ignore

    
 
