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

        # 타일맵을 굽자
        self._tilemap_surface = self.prepare_tilemap()

    def update(self):
        EntityManager.update()

    def draw(self, surface: pygame.Surface):
        # Background
        surface.fill(pygame.Color(0, 255, 170))
        Fonts.get("debug").render_to(
            surface,
            (700, 20),
            "GameScene",
            size=20,
        )
        Fonts.get("debug").render_to(
            surface,
            (600, 40),
            "(src/scenes/game_scene.py)",
        )

        # Tilemap
        surface.blit(self._tilemap_surface, (0, 0))

        EntityManager.draw(surface)

    def on_destroy(self):
        pass

    def prepare_tilemap(self):
        tileset = ResourceLoader.load_tileset("generic_1")
        _ = None
        return tileset.make_tilemap_surface(
            [
                [6, _, _, _, _, _, _, _, _, _, _, _, _, _],
                [6, _, _, _, _, _, _, _, _, _, _, _, _, _],
                [6, _, 2, 2, _, _, _, _, _, _, _, _, _, _],
                [6, _, _, _, _, _, _, _, _, _, _, _, _, _],
                [6, _, _, _, 2, 2, _, _, _, _, _, _, _, _],
                [6, _, _, _, 6, 6, _, 2, 2, _, _, _, _, _],
                [6, _, _, _, _, _, _, _, _, _, 2, _, _, _],
                [6, _, _, _, _, _, _, _, _, _, 6, 2, 2, _],
                [6, _, _, _, _, _, _, _, _, _, _, _, _, _],
                [6, 2, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            ]
        )
