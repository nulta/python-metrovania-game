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
from pygame import Surface, Vector2



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
        t = util.clamp(self.scene_time / 8, 0, 3)
        t1 = util.easeinout(t)

        cloud_offset = math.sin(self.scene_time / 3) * 30

        self.draw_parallax(surface, "background/intro/sky.png", 1.0, t1)
        self.draw_parallax(surface, "background/intro/stardust.png", 0.8, t1, True)
        self.draw_parallax(surface, "background/intro/cloud.png", 1.3, t1, True, cloud_offset)
        self.draw_parallax(surface, "background/intro/building1.png", 1.5, t1)
        self.draw_parallax(surface, "background/intro/building2.png", 2.3, t1)
        self.draw_parallax(surface, "background/intro/building3.png", 3.0, t1)

        t2 = util.easeout(t - 1.0)

        frame = ResourceLoader.load_image("background/intro/frame.png").copy()
        frame.set_alpha(round(t2 * 255))
        surface.blit(frame, (0, 0))

        t3 = util.clamp(t*2 - 3.0, 0, 1)
        t31 = util.remap(t3, (0, 0.1), (0,1))
        t32 = util.remap(t3, (0.05, 0.15), (0,1))
        t33 = util.remap(t3, (0.1, 0.2), (0,1))
        t34 = util.remap(t3, (0.15, 0.25), (0,1))

        if t31:
            img = ResourceLoader.load_image("background/intro/title.png")
            if t31 != 1:
                img = img.copy()
                img.set_alpha(round(t31 * 255))
            surface.blit(img, (0, 0))

        if t32:
            img = ResourceLoader.load_image("background/intro/text_start.png").copy()
            if t32 != 1:
                img = img.copy()
                img.set_alpha(round(t32 * 255))
            surface.blit(img, (0, 0))

        if t33:
            img = ResourceLoader.load_image("background/intro/text_options.png").copy()
            if t33 != 1:
                img = img.copy()
                img.set_alpha(round(t33 * 255))
            surface.blit(img, (0, 0))

        if t34:
            img = ResourceLoader.load_image("background/intro/text_quit.png").copy()
            if t34 != 1:
                img = img.copy()
                img.set_alpha(round(t34 * 255))
            surface.blit(img, (0, 0))


    
    def draw_parallax(self, surface: "Surface", image_name: "str", parallax_mul: "float",
                      t: "float", to_end=False, y_offset=0.0):
        image = ResourceLoader.load_image(image_name)
        initial_offset = -Vector2(0, 1490 - 600)
        offset = initial_offset - Vector2(0, t * initial_offset.y * parallax_mul)
        offset += Vector2(0, y_offset)
        if to_end:
            offset += Vector2(0, initial_offset.y * parallax_mul - initial_offset.y)

        surface.blit(image, offset)


    def on_destroy(self):
        pygame.mixer.music.unload()

    def press_button(self, button_index):
        if button_index == 0:
            # 새 게임
            from scene_manager import SceneManager
            from .player_choose import ChooseScene
            SceneManager.clear_scene()
            SceneManager.push_scene(ChooseScene())
        elif button_index == 1:
            # 설정
            pass
        else:
            # 게임 종료
            game_globals.exit = True
