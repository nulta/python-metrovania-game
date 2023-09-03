from typing import Sequence
import pygame
from constants import *
import json

"""
# 맵 파일 구조 (JSON)

{
    "tileset_name": "generic_1",
    "map_data": [
        [1, 2, 3, 4, 5, null],
        [null, null, null, null, null, null]
    ],
    "entities": [
        ["enemy", 0, 1]
    ],
    "music": "title.ogg",
    "background_img": "intro.png"
}
"""

class LevelData:
    def __init__(self):
        # 타일셋 이름
        self.tileset_name: "str" = "generic_1"

        # 타일맵
        self.map_data: "Sequence[Sequence[int | None]]" = [[None]]
        
        # [(엔티티 이름, 타일맵 X좌표, 타일맵 Y좌표)]
        self.entities: "Sequence[tuple[str, int, int]]" = []

        # 음악 파일 이름
        self.music: "str | None" = None

        # 배경 이미지 이름
        self.background_img: "str | None" = None


class Level:
    def __init__(self, level_data: "LevelData"):
        from resource_loader import ResourceLoader
        self._map_data = level_data.map_data
        self._tileset = ResourceLoader.load_tileset(level_data.tileset_name)
        self._entities = level_data.entities
        self._music = level_data.music
        if level_data.background_img:
            image_path = "sprites/background/" + level_data.background_img
            self._background = ResourceLoader.load_image_2x(image_path)
        else:
            self._background = pygame.Surface(GAME_WINDOW_SIZE)
            self._background.fill((255, 255, 255))
    
