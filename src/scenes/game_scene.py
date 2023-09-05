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
        self._background = self._level._background

        # 엔티티 관련 처리
        EntityManager.initialize()
        level.create_entities()

        # 타일맵 굽기
        self._tilemap_surface = level.get_tilemap_surface()


    def update(self):
        EntityManager.update()

    def draw(self, surface: pygame.Surface):
        camera_pos = game_globals.camera_offset

        # Background
        surface.blit(self._background, (0, 0))

        # Tilemap
        surface.blit(self._tilemap_surface, -camera_pos)

        EntityManager.draw(surface, camera_pos)

    def on_destroy(self):
        pass
    
    def camara(self):
        pass