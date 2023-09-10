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

    def draw_background(self, surface: pygame.Surface, scence):
        # 배경 그리기
        scence_path = ResourceLoader.load_image(f"background/black.png")
        surface.blit(scence_path, (0, 0))

    def draw(self, surface: pygame.Surface):
        t1 = util.on_keyframes(self.scene_time, {
            0.0: 0,
            8.0: 1,
        }, easein=True, easeout=True)
        # t1 = util.easeinout(t)

        cloud_offset = math.sin(self.scene_time / 3) * 30

        self.draw_parallax(surface, "background/intro/sky.png", 1.0, t1)
        self.draw_parallax(surface, "background/intro/stardust.png", 0.8, t1, True)
        self.draw_parallax(surface, "background/intro/cloud.png", 1.3, t1, True, cloud_offset)
        self.draw_parallax(surface, "background/intro/building1.png", 1.5, t1)
        self.draw_parallax(surface, "background/intro/building2.png", 2.3, t1)
        self.draw_parallax(surface, "background/intro/building3.png", 3.0, t1)

        t2 = util.on_keyframes(self.scene_time, {
            6.0: 0,
            8.0: 1,
        })

        frame = ResourceLoader.load_image("background/intro/frame.png")
        frame.set_alpha(round(t2 * 255))
        surface.blit(frame, (0, 0))

        t3 = util.on_keyframes(self.scene_time, {
            7.9: 0,
            8.0: 0.25,
            8.1: 0.5,
            8.2: 0.75,
            8.3: 1,
        })

        t31 = util.remapc(t3, (0, 0.25), (0,1))

        if t31:
            img = ResourceLoader.load_image("background/intro/title.png")
            if t31 != 1:
                img.set_alpha(round(t31 * 255))
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
        # 음악은 다음 씬과 이어진다.
        pass

