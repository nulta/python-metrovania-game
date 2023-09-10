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


class CreditsScene(Scene):
    """CreditsScene은 게임 타이틀 화면이다."""

    _music = ""
    def __init__(self):
        super().__init__()

        # 음악을 재생한다.
        Audio.music_set(self._music)

        # 메뉴창 UI와 관련된 변수들.
    def update(self):
        pass
    def draw_parallax(self, surface: "Surface", image_name: "str", parallax_mul: "float",
                      t: "float", to_end=False, y_offset=0.0):
        image = ResourceLoader.load_image(image_name)

        initial_offset = -Vector2(0, 4300 - 600)
        offset = initial_offset - Vector2(0, t * initial_offset.y * parallax_mul)
        offset += Vector2(0, y_offset)
        if to_end:
            offset += Vector2(0, initial_offset.y * parallax_mul - initial_offset.y)

        surface.blit(image, offset)
                     
    def draw(self, surface: pygame.Surface):
        t = util.on_keyframes(self.scene_time, {
            0.0: 1,
            10.0: 0,
        }, easein=False, easeout=False)

        self.draw_parallax(surface, "background/credit.png", 1.0, t)

    def on_destroy(self):
        # 음악은 다음 씬과 이어진다.
        pass

