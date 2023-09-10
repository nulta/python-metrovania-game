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

    def draw(self, surface: "Surface"):
        self.draw_background(surface, self.background_image)
        self.draw_box(surface)
        self.draw_info(surface)
        self.draw_skip(surface)
        self.draw_line(surface)
        self.draw_next(surface)


    def draw_background(self, surface: pygame.Surface, scence):
        # 배경 그리기
        scence_path = ResourceLoader.load_image(f"background/{scence}.png")
        surface.blit(scence_path, (0, 0))

    def draw_box(self, surface: pygame.Surface):
        # 박스 그리기
        scence_path = ResourceLoader.load_image(f"background/story_box.png")
        surface.blit(scence_path, (0, 0))



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


            
    def draw_line(self, surface: pygame.Surface):
        # 대사 그리기
        text = self.lines[self.line_count][1]
        font_size = 18
        color = (0, 0, 0)
        y_offset = 6
        line_changes = text.split('\n')
        if self.lines[self.line_count][0]=="blank":
            self.position_x = 110
            self.storyboard_path = ResourceLoader.load_image("story_board/blank.png")

        elif self.lines[self.line_count][0] =="player":
            self.position_x = 330
            gender = game_globals.player_gender
            if gender ==0:
                self.storyboard_path = ResourceLoader.load_image("story_board/male/player.png")
            elif gender ==1:
                self.storyboard_path = ResourceLoader.load_image("story_board/female/player.png")     

        else:
            self.position_x = 330
            self.storyboard_path = ResourceLoader.load_image(f"story_board/{self.lines[self.line_count][0]}.png")
        surface.blit(self.storyboard_path, (0, 0))

            

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
            "ENTER or Space 키를 누르면 다음 대사로 넘어간다",
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
    music_name = ""
    background_image = "war2"
    storyboard_image = ""
    next_level = "0_tutorial"

    lines = [
    ("blank","20xx년.세상은 한 사람에 의해 멸망했다."),
    ("blank","이름도 알려지지 않은 그 사람은 어디에서도 보지 못한 최첨단 무기와\n 생체 병기들을 이용해서 인간 문명을 공격."),
    ("blank","그 결과 인류는 20%도 채 남지 않게 되었다."),
    ("blank","몇 안되는 인간들은 살기 위해 모였다."),
    ("blank","그들은 수 년간의 고통을 견뎌내며\n'어비스' 이라 불리는 인류의 마지막 쉘터를 구축하게 되었다..."),
    ("blank","어비스는 인간들의 협동심과 하나 된 마음 아래 빠르게 안정을 찾게 되었고,\n 사건의 흑막인 '그 사람'의 공격은 이후로는 더 발생하지 않았다."),
    ("blank","그렇게 인류는 다시 평화를 찾게 된 것이다..."),
        ("player","할아버지..."),
        ("parksan","왜 그러냐, 지안아?"),
        ("player","이게 다 뭐예요... 저희 집 지하실에 이런 장소가 있었어요?\n 할아버지가 만든 거예요?"),
        ("parksan","당연하지. 언제 또 그것들이 우리를 죽이러 올지 모르니까\n 대비를 하는거야."),
        ("player","언제적 일인데 그게. 이상한 옷이나 입으라고 하고..."),
        ("parksan","투정은 됐다."),
        ("parksan","이곳은 너의 훈련을 위해 만든 곳이야.\n그 옷도 너만을 위해서 만들었고."),
        ("parksan","오늘은 침공 시 대피 훈련을 할 거다.\n할아버지가 매일 뭐라고 했었지?"),
        ("player","빨리 움직여서 안전한 곳으로 가라고요."),
        ("parksan","그래.\n 이 곳에는 실제 침공 현장과 같은 함정이 준비되어 있단다.\n 그것들을 피해서 안전한 곳으로 도착해 보거라."),
        ("player","네.. 빨리 끝내고 놀러 갈거예요."),
        ("parksan","그래. 할 건 끝내고 놀아라. 다 너를 위해서 하는 말이야."),
            ]
    
    
    
    
 
