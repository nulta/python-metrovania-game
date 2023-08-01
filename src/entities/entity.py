from pygame import Surface
from pygame.math import Vector2
from constants import *

class Entity():
    def __init__(self):
        self._position = Vector2(0, 0)
        self._valid = True
        self._pivot = Vector2(0, 0)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value
    
    @property
    def valid(self):
        """이 개체가 유효한지 여부. 유효하지 않은 개체는 사용해서는 안 된다."""
        return self._valid
    
    @property
    def pivot(self):
        """
            이 엔티티가 가진 surface의 좌표 기준점.
            position과 함께, 이 엔티티가 실제로 화면에 그려질 위치를 결정한다.
        """
        return self._pivot

    # 아래는 자식 클래스에서 덮어쓸 함수 #

    def update(self):
        """매 프레임마다 실행된다. 자기 자신의 상태를 업데이트한다."""
        pass

    def surface(self) -> Surface:
        """화면에 그릴 surface를 반환한다."""
        pass

    # 아래는 Class가 기본으로 가질 동작 #

    def signal(self, signal_name: str, *args: any):
        """지정된 임의의 함수를 호출한다. 해당 이름의 함수가 없을 경우, 아무것도 하지 않는다."""
        attr = getattr(self, signal_name.__class__, None)
        if callable(attr):
            try:
                attr(*args)
            except TypeError as e:
                # 함수의 호출 인자 개수가 다른 경우 TypeError가 난다.
                # 따라서, TypeError가 난 경우 에러를 무시하고 대신 콘솔에 메세지를 띄워 준다.
                print(f"Entity.signal(): Got {repr(e)} while signalling '{signal_name}' on entity of type '{repr(self.__class__)}'.")

    def remove(self):
        """이 엔티티를 삭제하도록 요청한다. 실제 삭제는 나중 프레임에서 이루어진다."""
        self._valid = False
