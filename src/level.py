from typing import Sequence
import pygame
from constants import *
import entities

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
        self.tileset_name: "str" = "generic_0"

        # 타일맵
        self.map_data: "Sequence[Sequence[int]]" = [[0]]
        
        # [(엔티티 이름, 타일맵 X좌표, 타일맵 Y좌표, 생성자 인수값: 선택사항), ...]
        self.entities: "Sequence[tuple[str, int, int, dict[str, object] | None]]" = []

        # 음악 파일 이름
        self.music: "str | None" = None

        # 배경 이미지 이름
        self.background_img: "str | None" = None


class Level:
    def __init__(self, level_data: "LevelData"):
        from resource_loader import ResourceLoader
        self._tileset = ResourceLoader.load_tileset(level_data.tileset_name)
        self._tile_size = TILE_SIZE
        self._tilemap_surface = None
        self._collision_map = None
        self._map_data = level_data.map_data
        overlap_entities = self._tileset.get_overlap_entity_list_of_map(self._map_data)
        self._entities: "Sequence[tuple[str, int, int, dict[str, object] | None]]" = [*level_data.entities, *overlap_entities]

        self._music = level_data.music
        if level_data.background_img:
            image_path = "sprites/background/" + level_data.background_img
            self._background = ResourceLoader.load_image_2x(image_path)
        else:
            self._background = pygame.Surface(GAME_WINDOW_SIZE)
            self._background.fill((255, 255, 255))
    
    def get_collision_map(self) -> "Sequence[Sequence[pygame.Rect | None]]":
        """
        이 레벨의 충돌 맵을 받아온다.
        
        충돌 맵은 Rect 또는 None의 2차원 리스트이며, 물리 엔진에서 바닥과의 충돌 판정을 할 때 사용된다.
        """
        # return list(map(lambda row: list(map(bool, row)), self._map_data))
        if self._collision_map:
            return self._collision_map

        collision_map: "list[list[pygame.Rect | None]]" = []
        for y in range(len(self._map_data)):
            collision_map.append([])
            for x in range(len(self._map_data[y])):
                tile_idx = self._map_data[y][x]
                collision_rect = self._tileset.get_tile_collision_rect(tile_idx)
                if collision_rect:
                    collision_rect = collision_rect.move(pygame.Vector2(x, y) * self._tile_size)
                collision_map[y].append(collision_rect)
        self._collision_map = collision_map
        return collision_map

    
    def get_tilemap_surface(self) -> "pygame.Surface":
        """이 레벨의 타일맵이 그려진 Surface를 받아온다.
        
        최초 호출 시에는 새 Surface를 그리고, 이후 다시 호출 시에는 미리 그려놓은 surface를 반환한다."""
        if self._tilemap_surface:
            return self._tilemap_surface
        else:
            self._tilemap_surface = self._tileset.make_tilemap_surface(self._map_data)
            return self._tilemap_surface
    
    def create_entities(self):
        """이 맵의 엔티티들을 전부 생성하고 EntityManager에 등록한다."""
        for ent_info in self._entities:
            ent_name = ent_info[0]
            ent_pos = pygame.Vector2(ent_info[1], ent_info[2]) * self._tile_size
            ent_props = len(ent_info) > 3 and ent_info[3] or {}
            ent = self._make_entity(ent_name, ent_props)
            if ent:
                ent.position = ent_pos

    def _make_entity(self, entity_name: "str", props: "dict[str, object]" = {}):
        """
        특정 이름을 가진 엔티티를 생성한다. 생성자에 props 딕셔너리를 **kwargs 형태로 제공한다. 
        
        그런 이름의 엔티티가 없다면 None을 반환한다.
        생성자의 인자값 형태가 props과 맞지 않을 경우 None을 반환한다.
        """
        ent_class = getattr(entities, entity_name, None)
        if not ent_class or not issubclass(ent_class, entities.Entity):
            print(f"Level.make_entity: Entity '{entity_name}' not found!")
            return None

        try:
            # 이게... 맞나?
            ent_class._level = self  # Dependency Injection
            ent = ent_class(**props)
            return ent
        except TypeError as e:
            print(f"Level.make_entity: Got TypeError while creating entity '{entity_name}' using props:", props)
            print(e)
            return None
        finally:
            ent_class._level = None  # 제자리로
