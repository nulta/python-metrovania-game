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
        pass
    def on_destroy(self):
        # 음악은 다음 씬과 이어진다.
        pass

