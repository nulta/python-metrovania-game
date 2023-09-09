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
        EntityManager.initialize(current_level=self._level)
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
        self.draw_hp(surface)

        EntityManager.draw(surface, camera_pos)

    def draw_hp(self,surface: pygame.Surface):
        from entity_manager import EntityManager
        player = EntityManager.get_player()
        if not player: return  
        hp = player._hp
        pygame.draw.rect(surface, (0, 0, 0),[35,35,210,34])
        pygame.draw.rect(surface, (168, 28, 7),[40,39,hp,26])
        text = f"hp:{hp}"
        font_size = 20
        color = (255, 255, 255)

        Fonts.get("bold").render_to(
            surface,
            (44,43),
            text,
            fgcolor=color,
            size=font_size,
        )


    def on_destroy(self):
        pass
    
    def camara(self):
        pass