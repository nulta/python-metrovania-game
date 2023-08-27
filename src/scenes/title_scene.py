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

class TitleScene(Scene):
    """TitleScene은 게임 타이틀 화면이다."""

    _music = "sounds/music/title.ogg"
    _button_texts = ["새 게임", "설정", "게임 종료"]

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
        if InputManager.pressed(ACTION_UP):
            Audio.common.select()
            self._focus_index -= 1
        elif InputManager.pressed(ACTION_DOWN):
            Audio.common.select()
            self._focus_index += 1
        self._focus_index %= len(self._button_texts)

        # 메뉴 입력 처리 (키보드)
        if InputManager.pressed(ACTION_CONFIRM):
            Audio.common.confirm()
            self.press_button(self._focus_index)

    def draw(self, surface: pygame.Surface):
        anim_progress = self.scene_time / 6

        # 배경 그리기
        if True:
            color_mul = int(util.lerpc(anim_progress, 0.5, 1) * 255)
            block_height = util.lerpc(anim_progress / 1.5, 260, 200)
            block_height += int(math.cos(game_globals.game_time * 0.5) * 3)

            surface.fill(pygame.Color(0, 100, 170))
            for i in range(2):
                surface.fill(
                    pygame.Color(0, 140 - i*20, 170),
                    (0, i*block_height, 800, block_height)
                )
            
            surface.fill((color_mul,) * 3, special_flags=pygame.BLEND_MULT)

        # 사람 그리기
        if True:
            color_mul = int(util.lerpc(anim_progress, 0, 0.9) * 255)
            human_y = int(util.lerpc(util.easeout(anim_progress / 1.5), 500, 210)) + 62
            human_y += int(math.cos(game_globals.game_time * 1.8) * 2)

            sprite_human = ResourceLoader.load_image_2x("sprites/player/female/idle.png").copy()
            sprite_human.fill((color_mul,) * 3, special_flags=pygame.BLEND_MULT)
            surface.blit(sprite_human, (330+130, human_y))

        # 소품 그리기
        if True:
            color_mul = int(util.lerpc(anim_progress, 0, 0.9) * 255)
            building_y = int(util.lerpc(util.easeout(anim_progress / 1.5), 500, 210))

            sprite_building = ResourceLoader.load_image_2x("sprites/background/building.png").copy()
            sprite_building.fill((color_mul,) * 3, special_flags=pygame.BLEND_MULT)
            surface.blit(sprite_building, (330, building_y))

        # 게임 이름 그리기
        Fonts.get("bold").render_to(
            surface,
            (25, 160),
            "플랫포머 게임(가제)",
            fgcolor=(255, 255, 255),
            size=50,
        )

        # 메뉴 목록 그리기
        for idx, text in enumerate(self._button_texts):
            font_size = 24
            y_offset = idx * (font_size + 6) + (math.sin(self.scene_time * 2.5 + idx/2) * 5)
            focused = self._focus_index == idx
            color = (0, 220, 255) if focused else (255, 255, 255)

            Fonts.get("bold").render_to(
                surface,
                (30, 460 + y_offset),
                text,
                fgcolor=color,
                size=font_size,
            )

    def on_destroy(self):
        pygame.mixer.music.unload()

    def press_button(self, button_index):
        if button_index == 0:
            # 새 게임
            from scene_manager import SceneManager
            from .game_scene import GameScene
            SceneManager.clear_scene()
            SceneManager.push_scene(GameScene(None))
        elif button_index == 1:
            # 설정
            pass
        else:
            # 게임 종료
            game_globals.exit = True
