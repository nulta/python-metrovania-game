import pygame
from resource_loader import ResourceLoader
import game_globals
from .scene import Scene
from entity_manager import EntityManager
from entities import Player
from constants import *
from fonts import Fonts
from level import Level

class GameScene(Scene):
    """GameScene은 인게임 씬이다."""

    def __init__(self, level: Level):
        super().__init__()
        self._level = level

        # 엔티티 관련 처리
        EntityManager.initialize()
        player = Player()
        player.position = pygame.Vector2(200, 200)

        # 타일맵을 굽자
        self._tilemap_surface = level.get_tilemap_surface()

    def update(self):
        EntityManager.update()

    def draw(self, surface: pygame.Surface):
        camera_pos = game_globals.camera_offset

        # Background
        surface.fill(pygame.Color(100, 200, 255))
        Fonts.get("debug").render_to(
            surface,
            (700, 20),
            "GameScene",
            size=20,
        )
        Fonts.get("debug").render_to(
            surface,
            (600, 40),
            str(camera_pos),
        )

        # Tilemap
        surface.blit(self._tilemap_surface, (-camera_pos[0], -camera_pos[1]))

        EntityManager.draw(surface, camera_pos)

    def on_destroy(self):
        pass
    
    def camara(self):
        pass