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
    def draw(self):
        # 어카냐
        pass

"""
# draw 처리를 어떻게 해야 할까
Solution 1. 모든 Entity가 Surface를 가진다.
            이 Surface를 draw 시점에서 자동으로 그려 준다.
            Pro: Con:
Solution 2. 모든 Entity가 화면에 직접 그린다.
            draw의 param으로 화면 Surface를 던져 준다.
Solution 3. draw 함수가 Surface를 반환한다.
"""
