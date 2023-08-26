import pygame
from resource_loader import ResourceLoader
from .scene import Scene
from entity_manager import EntityManager
from entities import Player
from constants import *
from fonts import Fonts

class GameScene(Scene):
    """GameScene은 인게임 씬이다."""

    def __init__(self, map):
        super().__init__()
        self._map = map

        # 엔티티 관련 처리
        EntityManager.initialize()
        player = Player(GENDER_FEMALE)
        player.position = pygame.Vector2(200, 200)

    def update(self):
        EntityManager.update()

    def draw(self, surface: pygame.Surface):
        surface.fill(pygame.Color(0, 255, 170))
        Fonts.get("debug").render_to(
            surface,
            (670, 20),
            "GameScene",
            size=20,
        )
        Fonts.get("debug").render_to(
            surface,
            (570, 40),
            "(src/scenes/game_scene.py)",
        )
        EntityManager.draw(surface)

    def on_destroy(self):
        pass
