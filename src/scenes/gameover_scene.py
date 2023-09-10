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


class GameOverScene(Scene):
    """GameOverScene은 게임 오버 화면이다.
    
    단독으로 사용하지 말고 다른 씬의 위에 올리도록 하자.
    """

    def __init__(self):
        super().__init__()
        from entity_manager import EntityManager

        prev_scene = EntityManager.game_scene
        assert prev_scene
        self._prev_scene = prev_scene

        Audio.music_set_volume(0.5)

    def update(self):
        # Enter 키
        if InputManager.pressed(ACTION_CONFIRM) or InputManager.pressed(ACTION_RELOAD_MAP):
            Audio.common.confirm()
            self.retry()
        
        # 이 아래 씬도 업데이트해준다.
        self._prev_scene.update()


    def draw(self, surface: pygame.Surface):
        Fonts.get("bold").render_to(
            surface,
            (100, 160),
            "X_X",
            fgcolor=(255, 255, 255),
            size=50
        )

        Fonts.get("bold").render_to(
            surface,
            (100, 220),
            "R 키를 눌러 재시작",
            fgcolor=(200, 200, 200),
            size=20,
        )

    def on_destroy(self):
        Audio.music_set_volume(1.0)

    def retry(self):
        self.remove()
        self._prev_scene.initialize_level()

