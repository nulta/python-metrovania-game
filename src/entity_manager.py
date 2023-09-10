from entities import *
from typing import Optional, Dict, TYPE_CHECKING
from pygame import Vector2, Surface, Rect
from util import classproperty

if TYPE_CHECKING:
    from level import Level
    from scenes.game_scene import GameScene

class EntityManager():
    """게임 내의 모든 Entity를 관리한다."""

    _ents: Dict[int, Entity] = {}
    _last_ent_key = 0
    _current_level: "Level | None" = None

    @classmethod
    def get_entity(cls, id: int) -> Optional[Entity]:
        """특정 ID의 Entity를 반환한다."""
        return cls._ents.get(id)

    @classmethod
    def push_entity(cls, ent: Entity):
        """새로운 Entity를 EntityManager에 등록한다."""
        id = cls._last_ent_key
        cls._last_ent_key += 1
        ent._id = id
        cls._ents[id] = ent

    @classmethod
    def get_player(cls) -> "Optional[Player]":
        """Player 개체를 반환한다."""
        for ent in cls._ents.values():
            if isinstance(ent, Player):
                return ent
        return None
    
    @classmethod
    def get_boss(cls) -> "Optional[Enemy]":
        """Player 개체를 반환한다."""
        for ent in cls._ents.values():
            if isinstance(ent, Enemy) and ent.get("is_boss", False):
                return ent
        return None
    
    @classmethod
    def get_static_entities(cls) -> "list[Entity]":
        return list(filter(lambda ent: ent.is_static, cls._ents.values()))
    
    @classmethod
    def find_colliding_entities(cls, rect_or_ent: "Rect | Entity") -> "list[Entity]":
        """주어진 Rect 또는 엔티티와 히트박스가 겹치는 엔티티를 찾는다."""
        rect = None
        ent = None
        if isinstance(rect_or_ent, Entity):
            rect: "Rect | None" = rect_or_ent.get("hitbox")
            ent = rect_or_ent
            if not rect:
                return []
        else:
            rect = rect_or_ent
            ent = None

        colliding = []
        for find_ent in cls._ents.values():
            hitbox = find_ent.get("hitbox")
            if not hitbox: continue
            if find_ent == ent: continue
            if not rect.colliderect(hitbox): continue
            colliding.append(find_ent)
        return colliding

    @classmethod
    def update(cls):
        # 유효하지 않은 개체를 전부 삭제한다
        for entid in list(cls._ents):
            if not cls._ents[entid].valid:
                del cls._ents[entid]

        # 모든 개체를 업데이트
        for ent in list(cls._ents.values()):
            ent.update()

    @classmethod
    def draw(cls, screen: "Surface", camera_pos: "Vector2"):
        for ent in cls._ents.values():
            # 2px 그리드에 정확하게 들어맞도록 위치를 내림한다.
            draw_pos = ent.position - ent.pivot - camera_pos
            draw_pos = draw_pos * 2 // 2

            ent_surface = ent.surface()
            screen.blit(ent_surface, draw_pos)

    @classmethod
    def initialize(cls, current_level: "Level | None" = None, game_scene: "GameScene | None" = None):
        """EntityManager를 깨끗하게 초기화한다!"""
        for ent in cls._ents.values():
            ent.remove()
        cls._current_level = current_level
        cls._game_scene = game_scene
        cls._ents = {}
        cls._last_ent_key = 0

    @classproperty
    def current_level(cls) -> "Level | None":
        """현재 활성 레벨을 받아온다."""
        # 진짜로 이게 최선인가?
        return cls._current_level

    @classproperty
    def game_scene(cls) -> "GameScene | None":
        """현재 활성 레벨을 받아온다."""
        # 진짜로 이게 최선인가?
        return cls._game_scene
