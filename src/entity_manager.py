from entities import *
from typing import Optional, Dict

class EntityManager():
    """게임 내의 모든 Entity를 관리한다."""

    _ents: Dict[int, Entity] = {}
    _last_ent_key = 0

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
    def get_enemy(cls) -> "Optional[Enemy]":
        """Enemy 개체를 반환한다."""
        for ent in cls._ents.values():
            if isinstance(ent, Enemy):
                return ent
        return None

    @classmethod
    def get_grenade_enemy(cls) -> "Optional[Grenade_enemy]":
        """Poison 개체를 반환한다."""
        for ent in cls._ents.values():
            if isinstance(ent, Grenade_enemy):
                return ent
        return None

    @classmethod
    def get_grenade_player(cls) -> "Optional[Grenade_player]":
        """Poison 개체를 반환한다."""
        for ent in cls._ents.values():
            if isinstance(ent, Grenade_player):
                return ent
        return None

    @classmethod
    def get_poison(cls) -> "Optional[Poison]":
        """Poison 개체를 반환한다."""
        for ent in cls._ents.values():
            if isinstance(ent, Poison):
                return ent
        return None

    @classmethod
    def get_bullet(cls) -> "Optional[Bullet]":
        """Poison 개체를 반환한다."""
        for ent in cls._ents.values():
            if isinstance(ent, Bullet):
                return ent
        return None

    @classmethod
    def get_fire(cls) -> "Optional[Fire]":
        """Poison 개체를 반환한다."""
        for ent in cls._ents.values():
            if isinstance(ent, Fire):
                return ent
        return None

    @classmethod
    def update(cls):
        # 유효하지 않은 개체를 전부 삭제한다
        for entid in list(cls._ents):
            if not cls._ents[entid].valid:
                del cls._ents[entid]

        # 모든 개체를 업데이트
        for ent in cls._ents.values():
            ent.update()

    @classmethod
    def draw(cls, screen: Surface):
        camera_pos = game_globals.camera_offset
        for ent in cls._ents.values():
            draw_pos = ent.position - ent.pivot
            draw_pos = (draw_pos[0] - camera_pos[0], draw_pos[1] - camera_pos[1])
            ent_surface = ent.surface()
            screen.blit(ent_surface, draw_pos)

    @classmethod
    def initialize(cls):
        """EntityManager를 깨끗하게 초기화한다!"""
        for ent in cls._ents.values():
            ent.remove()
        cls._ents = {}
        cls._last_ent_key = 0
