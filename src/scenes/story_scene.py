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
    story_scene=""

    name_table ={
        "blank":"","player": "지안","fanboy":"서큘레이터",
        "grenade":"B.W","hotman":"파에톤","navylady":"안티라이트",
        "parksan":"박사","speed":"제트네스"
    }

    def __init__(self):
        super().__init__()
        self.line_count=0

        # 음악을 재생한다.
        Audio.music_set(self.music_name)


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
        if not self.next_level:
            if not self.story_scene:
                from scene_manager import SceneManager
                from .credits_scene import CreditsScene
                SceneManager.clear_scene()
                SceneManager.push_scene(CreditsScene())
            else:
                scene = globals()[self.story_scene]
                assert issubclass(scene, StoryScene)
                SceneManager.clear_scene()
                SceneManager.push_scene(scene())
        else:
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

        name_text = self.name_table[self.lines[self.line_count][0]]
        name_font_size = 20
        Fonts.get("debug").render_to(
            surface,
            (300, 343),
            name_text,
            fgcolor=color,
            size=name_font_size,
        )


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
        # Audio.music_set("")
        pass


class StorySceneIntro(StoryScene):
    music_name = ""
    background_image = "boom"
    story_scene = "StorySceneIntro_1"
    lines = [
    ("blank","20xx년.\n세상은 한 사람에 의해 멸망했다."),
    ("blank","이름도 알려지지 않은 그 사람은 어디에서도 보지 못한\n최첨단 무기와 생체 병기들을 이용해서 인간 문명을 공격."),
    ("blank","그 결과 인류는 20%도 채 남지 않게 되었다.")
    ]            


class StorySceneIntro_1(StoryScene):
    music_name = ""
    background_image = "intro"
    story_scene = "Eye_Down"

    lines = [
    ("player","나는 그 사건 이후로 태어났다."),
    ("player","인간으로서 기본적으로 누려야 할\n인권, 행복, 가족 따위는 없었다."),
    ]

class Eye_Down(StoryScene):
    music_name = ""
    background_image = "eye1"
    story_scene = "Eye_Up"
    lines = [
    ("blank","나는 그래서 이 사건의 근원인 그 사람을 없애고 싶다."),
    ("blank","그들이 타고 온 타임머신을 빼앗아서 \n과거로 간다.\n그리고 어린아이였을 그 사람의 씨앗을 없애버린다..."),
    ]

class Eye_Up(StoryScene):
    music_name = ""
    background_image = "eye2"
    story_scene = "Black"

    lines = [   
    ("blank","나의 목표는 그것뿐이다")
    ]
class Black(StoryScene):
    music_name = ""
    background_image = "black"
    story_scene = "Before_gun"

    lines = [
    ("blank","..."),
    ("blank",".......")

    ]

class Before_gun(StoryScene):
    music_name = ""
    background_image = "parksan"
    next_level = "0_tutorial"

    lines = [
    ("parksan","내가 도움을 주마"),
    ("player","?"),
    ("parksan","내게 타임머신이 있다.\n이걸타고 과거로 가 놈을 해치우도록 해라"),
    ("parksan","나도 놈에게 가족을 잃었다.\n비록 이 타임머신을 개발하느라 늙어서 싸울 순 없지만..\n 이렇게라도 힘이 되고 싶구나.   "),
    ("parksan","이것도 가지고 가도록해라."),
     ("player","감사합니다"),

    ]

class Chapter_1(StoryScene):
    music_name = ""
    if game_globals.player_gender == GENDER_MALE:
        background_image = "male/stage_1_boss"
    else:
        background_image = "female/stage_1_boss"
    next_level = "1_fb85_boss"

    lines = [
    ("hotman","여기까지 무슨 일이지?"),
    ("player","저리 비켜. 퓨쳐리스트를 처리하러 왔다."),
    ("hotman","퓨쳐리스트 님을 처리한다고? 어림없지.\n절대 이 앞을 지나지 못할 것이다.")
    ]


class Chapter_2(StoryScene):
    music_name = ""
    if game_globals.player_gender == GENDER_MALE:
        background_image = "male/stage_2_boss"
    else:
        background_image = "female/stage_2_boss"
    next_level = "2_bt02_wind"

    lines = [
    ("fanboy", "파에톤를 쓰러트리다니 제법이군 이번엔 내가 상대해주마."),
    ("player","덤벼라..!"),
    ]

class Chapter_3(StoryScene):
    if game_globals.player_gender == GENDER_MALE:
        background_image = "male/stage_3_boss"
    else:
        background_image = "female/stage_3_boss"

    music_name = ""
    next_level = "3_sn91_speed"

    lines = [
    ("speed", "더이상 보스에게 가도록 두지 않겠다..!"),
    ("player","더 이상 나를 가로막지 마라.")
    ]

class Chapter_4(StoryScene):
    if game_globals.player_gender == GENDER_MALE:
        background_image = "male/stage_4_boss"

    else:
        background_image = "female/stage_4_boss"
    music_name = ""
    next_level = "4_sb87_grenade"

    lines = [
    ("grenade", "용케 여기까지 왔군. .  절대 더이상 못갈 것이다!"),
    ("player","마지막이라... 꽤나 강하겠군")
    ]
class Ending(StoryScene):
    music_name = ""
    background_image = "find"
    story_scene = "Ending_1"
    lines = [
    ("player","당신이 퓨처리스트..?"),
    ]
class Ending_1(StoryScene):
    music_name = ""
    background_image = "find_question"
    story_scene = "Ending_2"
    lines = [
    ("blank", "........."),
    ]
class Ending_2(StoryScene):
    music_name = ""
    background_image = "find_gun"
    story_scene = "Ending_Choose"
    lines = [
    ("blank", "인류의 적이 영영 사라지는 순간이었다.\n나는 그의 머리에 총을 겨눴다."),
    ("blank"," 선택의 순간이었다.\n인류의 최대악의 씨앗을 자를 것인가.\n 어린아이를 죽이는 비인도적인 일을 저지를것인가."),
    ]
class Ending_Choose(StoryScene):
    music_name = ""
    background_image = "find_gun"
    lines = [
     ("blank", "  "),
    ]
    def __init__(self):
        super().__init__()
        self._focus_index = 0

    def draw(self, surface: "Surface"):
        self.draw_background(surface, self.background_image)
        self.draw_box(surface)
        self.draw_info(surface)
        self.draw_line(surface)
        self.draw_choose(surface)

    def update(self):
        # 메뉴 이동 처리 (키보드)
        if InputManager.pressed(ACTION_UP):
            Audio.common.select()
            self._focus_index = 1

        elif InputManager.pressed(ACTION_DOWN):
            Audio.common.select()
            self._focus_index = 2

        # 메뉴 입력 처리 (키보드)
        if InputManager.pressed(ACTION_CONFIRM):
            Audio.common.confirm()
            self.press_button(self._focus_index)
        
    def press_button(self, button_index):
        if button_index == 1:
            #쏜다
            self.story_scene = "Ending_Shoot"
            Audio.common.select()
            self.next_scene()
        elif button_index == 2:
            #안 쏜다
            self.story_scene = "Ending_No_Shoot"
            Audio.common.select()
            self.next_scene()

    def draw_choose(self,surface: pygame.Surface):
        # 선택지 그리기
        font = 100
        font_select= 150
        color = (0,0,0)
        color_select = (0, 103, 163)       
        if self._focus_index == 0:
            color_shoot=color
            color_no_shoot=color
            size_shoot = font
            size_no_shoot =font

        elif self._focus_index == 1:
            color_shoot= color_select
            color_no_shoot=color
            size_shoot = font_select
            size_no_shoot =font
        else:
            color_shoot=color
            color_no_shoot=color_select
            size_shoot = font
            size_no_shoot =font_select

        Fonts.get("bold").render_to(
        surface,
        (110, 400),
        "쏜다",
        color_shoot,
        size_shoot
        )
        Fonts.get("bold").render_to(
        surface,
        (110, 450),
        "안 쏜다",
        color_no_shoot,
        size_no_shoot,
        )

    def draw_info(self,surface: pygame.Surface):
        # 안내문 그리기
        Fonts.get("bold").render_to(
            surface,
            (350, 555),
            "ENTER or Space를 눌러 선택합니다",
            fgcolor=(255, 255, 255),
            size=15,
        )

class Ending_Shoot(StoryScene):
    music_name = ""
    background_image = "story_box"
    lines = [
     ("blank", "퓨처리스트의 존재는 영영 사라졌고 인류는 자유를 되찾았다"),
     ("blank", "문명은 더없을 번영을 이루었고 자유와 행복과 함께 언제까지나 살아가게되었다."),

    ]
class Ending_No_Shoot(StoryScene):
    music_name = ""
    background_image = "happy_ending"
    lines = [
    ("blank", "나는 과거에 남아 그를 교화하기로 했다.\n 그에게 불교경전을 읽어주었고 그는 자비와 인에 대해 깨우치고 있는중이다."),
    ("blank", "문명은 더없을 번영을 이루었고 자유와 행복과 함께 언제까지나 살아가게되었다."),

     ]
    
