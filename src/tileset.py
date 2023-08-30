import pygame
from typing import Sequence

class Tileset:
    def __init__(self, tile_size: int, surface: pygame.Surface):
        tileset_w, tileset_h = surface.get_size()
        self._surface = surface
        self._tile_size = tile_size
        self._tile_dimensions = (tileset_w // tile_size, tileset_h // tile_size)

    def __len__(self):
        return self._tile_dimensions[0] * self._tile_dimensions[1]

    def _get_rect(self, tile_idx: int):
        assert tile_idx < len(self), "tile_idx must be less than the len(tileset)"
        tiles_x = self._tile_dimensions[0]

        tile_size = self._tile_size
        coord_x = tile_size * (tile_idx % tiles_x)
        coord_y = tile_size * (tile_idx // tiles_x)
        
        return pygame.Rect(coord_x, coord_y, tile_size, tile_size)

    def draw_tile(self, surface: pygame.Surface, dest: "tuple[int, int]", tile_idx: int):
        tile_area = self._get_rect(tile_idx)
        tileset_surface = self._surface
        surface.blit(tileset_surface, dest, tile_area)

    def make_tilemap_surface(self, map_data: "Sequence[Sequence[int|None]]"):
        size_w = self._tile_size * max(map(len, map_data))
        size_h = self._tile_size * len(map_data)
        surface = pygame.Surface((size_w, size_h), flags=pygame.SRCALPHA)
        
        # [(surface, coord, rect), ]
        blits_data = []
        for y, row in enumerate(map_data):
            for x, tile_idx in enumerate(row):
                if tile_idx is None: continue
                blits_data.append((
                    self._surface,
                    (x * self._tile_size, y * self._tile_size),
                    self._get_rect(tile_idx)
                ))

        surface.blits(blits_data, False)
        return surface


# TODO: 타일의 충돌 판정은?
