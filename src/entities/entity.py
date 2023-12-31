from pygame import Surface, Rect
from pygame.math import Vector2
from constants import *
from typing import TYPE_CHECKING, TypeVar, Any
import game_globals

if TYPE_CHECKING:
    from level import Level
    _T = TypeVar('_T')

class Entity():
    is_player = False
    is_enemy = False
    is_static = False
    always_update = False  # 화면 밖에서도 update()되게 한다.

    def __init__(self):
        from entity_manager import EntityManager
        self._id = -1
        self._position = Vector2(0, 0)
        self._valid = True
        self._pivot = Vector2(0, 0)

        # 생성될 때 자동으로 EntityManager에 등록된다.
        # self._id도 이 때 할당된다.
        EntityManager.push_entity(self)

    @property
    def position(self) -> Vector2:
        return self._position

    @position.setter
    def position(self, value: Vector2):
        self._position = Vector2(round(value.x), round(value.y))

    @property
    def valid(self):
        """이 개체가 유효한지 여부. 유효하지 않은 개체는 사용해서는 안 된다."""
        return self._valid

    @property
    def pivot(self) -> Vector2:
        """이 엔티티가 가진 surface의 좌표 기준점.

        position과 함께, 이 엔티티가 실제로 화면에 그려질 위치를 결정한다.
        """
        return self._pivot

    @property
    def id(self):
        """이 엔티티의 ID. EntityManager에서 관리한다."""
        return self._id

    # 아래는 자식 클래스에서 덮어쓸 함수 #

    def update(self):
        """매 프레임마다 실행된다. 자기 자신의 상태를 업데이트한다."""
        from entity_manager import EntityManager
        level = EntityManager.current_level

        if DEBUG_DRAW_HITBOX and not self.is_static:
            import debug
            hitbox = self.get("hitbox", Rect(0,0,0,0))
            debug.draw_rect(hitbox, on_map=True)
        
        if level and self.position.y > level.death_barrier:
            self.kill()

    def surface(self) -> Surface:
        """화면에 그릴 surface를 반환한다."""
        return Surface((0, 0))
    
    def on_suspend(self):
        """엔티티가 화면 밖으로 나가는 등 일시 정지되기 직전에 호출된다."""
        pass

    # 아래는 Class가 기본으로 가질 동작 #

    def call(self, signal_name: str, *args: object) -> "None | Any":
        """지정된 임의의 함수를 호출한다. 해당 이름의 함수가 없을 경우, 아무것도 하지 않는다."""
        attr = getattr(self.__class__, signal_name, None)
        if callable(attr):
            try:
                return attr(self, *args)
            except TypeError as e:
                # 함수의 호출 인자 개수가 다른 경우 TypeError가 난다.
                # 따라서, TypeError가 난 경우 에러를 무시하고 대신 콘솔에 메세지를 띄워 준다.
                print(f"Entity.call(): Got {repr(e)} while calling '{signal_name}' on entity of type '{repr(self.__class__)}'.")

    def get(self, property_name: str, default: "_T" = None) -> "Any | _T":
        """지정된 임의의 프로퍼티를 받아온다. 해당 이름의 프로퍼티가 없을 경우 default 값(기본 None)을 반환한다."""
        return getattr(self, property_name, default)

    def remove(self):
        """이 엔티티를 삭제하도록 요청한다. 실제 삭제는 나중 프레임에서 이루어진다."""
        self._valid = False

    def kill(self):
        """비 인간형 엔티티는 삭제하고, 인간형 엔티티는 죽인다."""
        self.remove()
