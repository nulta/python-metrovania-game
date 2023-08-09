from entities import *
from typing import Optional, Dict

class EntityManager():
    """게임 내의 모든 Entity를 관리한다."""

    _ents: Dict[int, Entity] = {}
    _last_ent_key = 0

    @classmethod
    def get_entity(cls, id: int) -> Optional[Entity]:
        return cls._ents.get(id)

    @classmethod
    def push_entity(cls, ent: Entity):
        cls._ents[cls._last_ent_key] = ent
        cls._last_ent_key += 1
    
    @classmethod
    def get_player(cls) -> Optional[Player]:
        # 일단은 O(N) 완전 탐색으로...
        for ent in cls._ents.values():
            if isinstance(ent, Player):
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
        for ent in cls._ents.values():
            draw_pos = ent.position - ent.pivot
            ent_surface = ent.surface()
            screen.blit(ent_surface, draw_pos)
