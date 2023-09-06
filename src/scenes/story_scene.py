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

    music_name = ""
    lines = []
    background_image = ""
    character_image = ""

    def __init__(self):
        assert self.__class__.next_scene != StoryScene.next_scene, (
            "The method 'next_scene()' should must be overriden."
        )

        super().__init__()
        self.line_count=0

        # 음악을 재생한다.
        if self.music_name:
            music = f"sounds/music/{self.music_name}.ogg"
            music_path = ResourceLoader.get_resource_path(music)
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(-1)


    def update(self):
        # 메뉴 이동 처리 (키보드)
        #건너뛰기
        if InputManager.pressed(ACTION_CANCEL):
            Audio.common.select()
            self.next_scene()
        #다음대사
        elif InputManager.pressed(ACTION_CONFIRM):
            Audio.common.select()
            self.line_count +=1
            if len(self.lines) == self.line_count:
                self.next_scene()
    
    def next_scene(self):
        """다음 씬으로 넘어간다.
        
        StoryScene을 상속하는 클래스는 **반드시** 이 함수를 재정의해야 한다.
        """
        raise NotImplementedError

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
        scence_path = ResourceLoader.load_image_2x(f"sprites/background/{scence}.png")
        surface.blit(scence_path, (0, 0))

    def draw_character(self, surface: pygame.Surface,character):
        if not character: return

        # 사람 그리기
        character_path = ResourceLoader.load_image_2x(f"sprites/story_character/{character}.png")
        surface.blit(character_path, (550, 200))

    def draw_stroyboard(self, surface: pygame.Surface):
        storyboard_path = ResourceLoader.load_image("sprites/background/storyboard.png")
        surface.blit(storyboard_path, (0, 0))

    def draw_skip(self, surface: pygame.Surface):
        # 건너뛰기 그리기
        pygame.draw.rect(surface,(0,0,0,100),[680,30,140,40],0)

        text = "건너뛰기(ESC)"
        font_size = 20
        color = (255, 255, 255)

        Fonts.get("bold").render_to(
            surface,
            (690, 40),
            text,
            fgcolor=color,
            size=font_size,
        )

    def draw_next(self, surface: pygame.Surface):
        # 다음대사 버튼 그리기
        text = "▼"
        font_size = 15
        color = (255, 255, 255)
        Fonts.get("bold").render_to(
            surface,
            (740, 400 + int(math.sin(self.scene_time*3)*6)),
            text,
            fgcolor=color,
            size=font_size,
        )

    def draw_line(self, surface: pygame.Surface):
        # 대사 그리기
        text = self.lines[self.line_count]
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
        Fonts.get("bold").render_to(
            surface,
            (300, 555),
            "ENTER를 눌러 진행합니다",
            fgcolor=(255, 255, 255),
            size=15,
        )

    def on_destroy(self):
        pygame.mixer.music.unload()


class StorySceneIntro(StoryScene):
    lines = ["ㅡ",
            "러ㅏㄹㄹ",
            "아ㅓ라ㅓ아러ㅏㅇ"
            ]
    
    _button_texts = ["건너뛰기(ESC)", "▽"]
    music_name = ""
    info_texts = ["ENTER 키를 누르면 다음 대사로 넘어간다",
                  "ESC 키를 누르면 이 장면이 스킵된다"]
    background_image = "intro"
    character_image = "fanboy"

    def next_scene(self):
        from scene_manager import SceneManager
        from resource_loader import ResourceLoader

        # TODO: 이거 정리
        leveldata = ResourceLoader.load_level_data("0_tutorial")
        level = Level(leveldata)
        scene = GameScene(level)
        SceneManager.clear_scene()
        SceneManager.push_scene(scene)
    
 
