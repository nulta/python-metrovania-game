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
    Text= "ㅇ\nㄹ\n나\n얼\n아\n러\nㅏ\nㄴ\nㅁ\nㅇ\n리\nㅏ\nㄴ\n어\n라\nㅣ\n넝\n라\nㅓ\nㅁ\nㄴ\n러\n나\nㅣ\nㅇ\n러\nㅏ\nㅣ\nㄴ\n어\n리\nㅏ\nㅁ\nㅇ\n너\n라\nㅣ\n넝\nㅁ\n라\nㅣ\n넘\nㅇ\n라\nㅣ\n"
    def __init__(self):
        super().__init__()

        # 음악을 재생한다.
        Audio.music_set(self._music)

        # 메뉴창 UI와 관련된 변수들.
    def update(self):
        pass
    def draw(self, surface: pygame.Surface):
        self.draw_background(surface)
        self.draw_text(surface)
    def draw_background(self, surface: pygame.Surface):
        # 배경 그리기
        scence_path = ResourceLoader.load_image(f"background/black.png")
        surface.blit(scence_path, (0, 0))

    def draw_text(self, surface: pygame.Surface):
        t = util.on_keyframes(self.scene_time, {
            0.0: 1,
            8.0: 0,
        }, easein=True, easeout=True)


        Fonts.get("bold").render_to(
            surface,
            (300, 555),
            self.Text,
            fgcolor=(255, 255, 255),
            size=15,
        )

    def on_destroy(self):
        # 음악은 다음 씬과 이어진다.
        pass

