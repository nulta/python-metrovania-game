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

    _music = "sounds/music/title.ogg"

    def __init__(self):
        super().__init__()
        from entity_manager import EntityManager

        prev_scene = EntityManager.game_scene
        assert prev_scene
        self._prev_scene = prev_scene

        # 음악을 재생한다.
        music_path = ResourceLoader.get_resource_path(self._music)
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)

    def update(self):
        # Enter 키
        if InputManager.pressed(ACTION_CONFIRM):
            Audio.common.confirm()
            self.retry()
        
        # 이 아래 씬도 업데이트해준다.
        self._prev_scene.update()


    def draw(self, surface: pygame.Surface):
        t = math.radians(self.scene_time * 360)
        dx = math.cos(t) * 50
        dy = math.sin(t) * 50

        Fonts.get("bold").render_to(
            surface,
            (100 + dx, 160 + dy),
            "GAME OVER",
            fgcolor=(230, 230, 230),
            size=50,
            rotation=round(self.scene_time * 360)
        )

        Fonts.get("bold").render_to(
            surface,
            (100, 260),
            "Press Enter",
            fgcolor=(200, 200, 200),
            size=20,
        )

    def on_destroy(self):
        pygame.mixer.music.unload()

    def retry(self):
        self.remove()
        self._prev_scene.initialize_level()

