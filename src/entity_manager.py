from entities import *
from typing import Optional, Dict

class EntityManager():
    """게임 내의 모든 Entity를 관리한다."""

    _ents: Dict[int, Entity] = {}
    _last_ent_key = 0

    @classmethod
    def get_entity(self, id: int) -> Optional[Entity]:
        return self._ents.get(id)

    @classmethod
    def push_entity(self, ent: Entity):
        self._ents[self._last_ent_key] = ent
        self._last_ent_key += 1
    
    @classmethod
    def update(self):
        # 유효하지 않은 개체를 전부 삭제한다
        for entid in list(self._ents):
            if not self._ents[entid].valid:
                del self._ents[entid]
        
        # 모든 개체를 업데이트
        for ent in self._ents.values():
            ent.update()
    
    @classmethod
    def draw(self, screen: Surface):
        for ent in self._ents.values():
            draw_pos = ent.position - ent.pivot
            ent_surface = ent.surface()
            screen.blit(ent_surface, draw_pos)
