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
    storyboard_image = ""
    next_level = ""
    boss_name = ""
    player_name = ""
    

    def __init__(self):
       # assert self.__class__.next_scene != StoryScene.next_scene, (
        #    "The method 'next_scene()' should must be overriden."
        #)

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
        from scene_manager import SceneManager
        from resource_loader import ResourceLoader
        leveldata = ResourceLoader.load_level_data(f"{self.next_level}")
        level = Level(leveldata)
        scene = GameScene(level)
        SceneManager.clear_scene()
        SceneManager.push_scene(scene)
        """다음 씬으로 넘어간다.
        
        StoryScene을 상속하는 클래스는 **반드시** 이 함수를 재정의해야 한다.
        """
        
        #raise NotImplementedError

    def draw(self, surface: "Surface"):
        self.draw_background(surface, self.background_image)
        self.draw_info(surface)
        self.draw_skip(surface)
        self.draw_storyboard(surface,self.storyboard_image)
        self.draw_line(surface,self.storyboard_image)
        self.draw_next(surface)

    def draw_background(self, surface: pygame.Surface, scence):
        # 배경 그리기
        scence_path = ResourceLoader.load_image(f"background/{scence}.png")
        surface.blit(scence_path, (0, 0))

    def draw_storyboard(self, surface: pygame.Surface,character):
        # 사람 그리기
        if not character:
            storyboard_path = ResourceLoader.load_image(f"story_board/blank.png")
            surface.blit(storyboard_path, (0, 0))

        elif character =="player":
            gender = game_globals.player_gender
            storyboard_path = ResourceLoader.load_image(f"story_board/{gender}/player.png")
            surface.blit(storyboard_path, (0, 0))

        else:
    
            storyboard_path = ResourceLoader.load_image(f"story_board/{character}.png")
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
        color = (0, 103, 163)
        Fonts.get("bold").render_to(
            surface,
            (740, 400 + int(math.sin(self.scene_time*3)*6)),
            text,
            fgcolor=color,
            size=font_size,
        )

    def draw_line(self, surface: pygame.Surface,character):
        # 대사 그리기
        text = self.lines[self.line_count]
        font_size = 18
        color = (0, 0, 0)
        y_offset = 6
        line_changes = text.split('\n')
        if not character:
            self.position_x = 110
        else:
            self.position_x = 330
            

        if not line_changes:
            Fonts.get("default").render_to(
                surface,
                (self.position_x, 400),
                text,
                fgcolor=color,
                size=font_size,
            )
        else:
            for line in line_changes:
                Fonts.get("default").render_to(
                    surface,
                    (self.position_x, 400 + y_offset),
                    line,
                    fgcolor=color,
                    size=font_size,
                    )
                y_offset += 10+ font_size
                



        

    def draw_info(self,surface: pygame.Surface):
        # 안내문 그리기
                  
        Fonts.get("bold").render_to(
            surface,
            (300, 555),
            "ENTER 키를 누르면 다음 대사로 넘어간다",
            fgcolor=(255, 255, 255),
            size=15,
        )
        Fonts.get("bold").render_to(
            surface,
            (320, 575),
            "ESC 키를 누르면 이 장면이 스킵된다",
            fgcolor=(255, 255, 255),
            size=15,
        )

    def on_destroy(self):
        pygame.mixer.music.unload()


class StorySceneIntro(StoryScene):
    boss_name = BOSS_NAME
    player_name = PLAYER_NAME
    doctor_name = DOCTOR_NAME
    lines = [
            f" 그 전쟁은 스스로 신의 자손이라 칭하는 악명높은 북조선의 테러리스트 {boss_name}가\n 북조선 정부를 침공하면서였다.",
            f" 이미 {boss_name}는 한반도를 중심으로 세력을 넓히고 있다.\n 세계 여러 나라가 그에게 덤볐음에도 속수무책이었다.",
            f" 그의 엄청난 기계화 부대와 6명의 간부들을 도저히 이길수 없었다. \n전 세계는 이제 {boss_name}의 손이 넘어갈 판이다.",
            f" 한편, 남한의 군사연구자인 {doctor_name}는 조수인 {player_name}은 타임머신을 통해 {boss_name}의 세력이\n 비교적 약한 과거로 보내 그를 미리 처치하려 한다. ",
            f" 이제 세계는 {player_name} 한명에게 달려있다.\n 하지만 {boss_name}도 그 계획을 이미 알아차리고 {player_name}에 맞설 준비를 하는데..",
             ]
    
    music_name = ""
    
    background_image = "war2"
    storyboard_image = "fanboy"
    next_level = "0_tutorial"
    
    
 
