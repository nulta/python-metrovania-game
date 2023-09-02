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


class TitleScene(Scene):
    """TitleScene은 게임 타이틀 화면이다."""

    _music = "  "
    _button_texts = ["건너뛰기", "설정"]

    def __init__(self):
        super().__init__()

        # 음악을 재생한다.
        music_path = ResourceLoader.get_resource_path(self._music)
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)

        # 메뉴창 UI와 관련된 변수들.
        self._focus_index = 0

    def update(self):
        # 메뉴 이동 처리 (키보드)
        if InputManager.pressed(ACTION_RIGHT):
            Audio.common.select()
            self._focus_index += 1
        elif InputManager.pressed(ACTION_LEFT):
            Audio.common.select()
            self._focus_index -= 1
        self._focus_index %= len(self._button_texts)

        # 메뉴 입력 처리 (키보드)
        if InputManager.pressed(ACTION_CONFIRM):
            Audio.common.confirm()
            self.press_button(self._focus_index,nextscene=list[Scene])

    def draw_background(self, surface: pygame.Surface, sence):
        # 배경 그리기
        if True:
            scence_path = ResourceLoader.load_image_2x(f"{sence}")
            surface.blit(scence_path, (0, 0))

    def draw_character(self, surface: pygame.Surface,character):
        # 사람 그리기
        if True:
            character_path = ResourceLoader.load_image_2x(f"{character}")
            surface.blit(character_path, (700, 300))

        #스트리보드 그리기
    def draw_stroyboard(self,surface: pygame.Surface):
        anim_progress = self.scene_time / 6
        if True:
            color_mul = int(util.lerpc(anim_progress, 0, 0.9) * 255)
            board_y = int(util.lerpc(util.easeout(anim_progress), 600, 0))

            sprite_storyboard = ResourceLoader.load_image_2x("sprites/background/storyboard.png").copy()
            sprite_storyboard.fill((color_mul,) * 3, special_flags=pygame.BLEND_MULT)
            surface.blit(sprite_storyboard, (330, board_y))
           
    def draw(self,surface: pygame.Surface):
        # 메뉴 목록 그리기
        for idx, text in enumerate(self._button_texts):
            font_size = 12
            x_offset = idx * (font_size + 6) + (math.sin(self.scene_time * 2.5 + idx/2) * 5)
            focused = self._focus_index == idx
            color = (0, 220, 255) if focused else (255, 255, 255)

            Fonts.get("bold").render_to(
                surface,
                (780, 30 + x_offset),
                text,
                fgcolor=color,
                size=font_size,
            )

    def on_destroy(self):
        pygame.mixer.music.unload()

    def press_button(self, button_index, nextscene):
        if button_index == 0:
            # 건너뛰기
            from scene_manager import SceneManager
            from .game_scene import GameScene
            SceneManager.clear_scene()
            SceneManager.push_scene(nextscene)

        elif button_index == 1:
            # 설정
            pass

 
