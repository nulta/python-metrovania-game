import pygame
from typing import Sequence, Any
from pygame import Rect

class Tileset:
    """타일셋 하나를 다루는 클래스.
    
    타일셋의 각 타일에는 번호(`tile_idx`)가 붙는다.
    번호는 1번부터 시작하며, 이미지 파일에서 맨 왼쪽 위 타일이 1번이다.
    최대 범위를 벗어나는 번호의 타일을 사용해서는 안 된다.

    수정: 번호는 1번부터 시작한다. 0번은 "빈 타일"을 나타내는 특수한 값으로 한다.
    """

    def __init__(self, tile_size: int, surface: pygame.Surface, metadata: "dict[str, Any] | None" = None):
        tileset_w, tileset_h = surface.get_size()
        self._surface = surface
        self._tile_size = tile_size
        self._tile_dimensions = (tileset_w // tile_size, tileset_h // tile_size)

        self._override_rect_tiles: "dict[int, Rect]" = {}
        self._overlap_entity_tiles: "dict[int, tuple[str, dict[str, Any]]]" = {}
        if metadata:
            if "override_rect" in metadata:
                rects: "dict[str, list[float]]" = metadata["override_rect"]
                convert_rect = lambda tup: Rect(*map(lambda x: x*tile_size, tup))
                self._override_rect_tiles = {
                    int(k): convert_rect(v)
                    for k, v in rects.items()
                }
            
            if "overlap_entity" in metadata:
                overlaps: "dict[str, tuple[str, dict[str, Any] | None]]" = metadata["overlap_entity"]
                self._overlap_entity_tiles = {
                    int(k): (v[0], v[1] if len(v)>1 and v[1] else {})
                    for k, v in overlaps.items()
                }


    def __len__(self):
        return self._tile_dimensions[0] * self._tile_dimensions[1] + 1

    def _get_rect(self, tile_idx: int):
        assert tile_idx < len(self)
        assert 1 <= tile_idx

        tile_idx -= 1
        tiles_x = self._tile_dimensions[0]
        tile_size = self._tile_size
        coord_x = tile_size * (tile_idx % tiles_x)
        coord_y = tile_size * (tile_idx // tiles_x)
        
        return pygame.Rect(coord_x, coord_y, tile_size, tile_size)

    def draw_tile(self, surface: pygame.Surface, dest: "tuple[int, int]", tile_idx: int):
        """타일 하나를 그린다."""
        if tile_idx == 0:
            return
        tile_area = self._get_rect(tile_idx)
        tileset_surface = self._surface
        surface.blit(tileset_surface, dest, tile_area)

    def make_tilemap_surface(self, map_data: "Sequence[Sequence[int]]"):
        """2차원 리스트에서 받아온 타일 정보로 그린 Surface를 반환한다.
        
        2차원 리스트의 칸 하나하나는 타일 하나하나와 대응된다.
        리스트의 원소가 int이면, 이는 타일 번호로 해석한다.
        리스트의 원소가 0이면, 그 칸에는 타일이 없음을 의미한다.

        @example
        ```
        tileset.make_tilemap_surface(
            [
                [6, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 2, 2, 2, 0],
                [6, 0, 0, 0, 0, 0],
                [6, 1, 1, 1, 1, 2],
            ]
        )
        ```
        """
        size_w = self._tile_size * max(map(len, map_data))
        size_h = self._tile_size * len(map_data)
        surface = pygame.Surface((size_w, size_h), flags=pygame.SRCALPHA)
        
        # [(surface, coord, rect), ]
        blits_data = []
        for y, row in enumerate(map_data):
            for x, tile_idx in enumerate(row):
                if tile_idx == 0: continue
                blits_data.append((
                    self._surface,
                    (x * self._tile_size, y * self._tile_size),
                    self._get_rect(tile_idx)
                ))

        surface.blits(blits_data, False)
        return surface
    
    def get_tile_collision_rect(self, tile_idx: int):
        if tile_idx == 0:
            return None
        elif tile_idx in self._override_rect_tiles:
            return self._override_rect_tiles[tile_idx]
        else:
            return Rect(0, 0, self._tile_size, self._tile_size)

    def get_overlap_entity_list_of_map(self, map_data: "Sequence[Sequence[int]]") -> "Sequence[tuple[str, int, int, dict[str, object]]]":
        conversion_table = self._overlap_entity_tiles
        if not conversion_table:
            return []
        
        entity_table: "list[tuple[str, int, int, dict[str, Any]]]" = []
        for y in range(len(map_data)):
            for x in range(len(map_data[y])):
                tile_id = map_data[y][x]
                if tile_id in conversion_table:
                    ent_name, ent_kwargs = conversion_table[tile_id]
                    entity_table.append((ent_name, x, y, ent_kwargs))
        
        return entity_table
