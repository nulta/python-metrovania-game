import pygame
from resource_loader import ResourceLoader
import game_globals
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
            "(src/scenes/game_scene.py)",
        )

        # Tilemap


        player = EntityManager.get_player()  # Player 또는 None
        if not player: return     
        tilemap_x = player.position.x // GAME_WINDOW_SIZE[0] * GAME_WINDOW_SIZE[0]
        game_globals.camera_offset = (tilemap_x, 0)
        camera_pos = game_globals.camera_offset
        surface.blit(self._tilemap_surface, (-camera_pos[0], camera_pos[1]))

        Fonts.get("debug").render_to(
            surface,
            (50, 20),
            f"{tilemap_x}",
            size=20,
        )


        EntityManager.draw(surface)

    def on_destroy(self):
        pass
    
    def prepare_tilemap(self):
        tileset = ResourceLoader.load_tileset("generic_1")
        _ = None
        return tileset.make_tilemap_surface(
            [
                [6, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
                [6, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
                [6, _, 2, 2, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
                [6, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
                [6, _, _, _, 2, 2, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
                [6, _, _, _, 6, 6, _, 2, 2, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
                [6, _, _, _, _, _, _, _, _, _, 2, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
                [6, _, _, _, _, _, _, _, _, _, 6, 2, 2, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
                [6, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
                [6, 2, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            ]
        )
    def camara(self):
        pass