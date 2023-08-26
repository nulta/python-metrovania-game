from pygame import Surface

class Scene():
    """Scene은 게임에 등장할 '장면'이다.
    타이틀 화면, 일시정지 화면, 게임 화면 등을 Scene으로 구현한다.
    self._valid가 False가 되면, 다음 프레임에서 이 Scene은 삭제된다.
    """

    def __init__(self):
        self._valid = True
        self._scene_time = 0.0

    @property
    def valid(self):
        """이 개체가 유효한지 여부. 유효하지 않은 개체는 사용해서는 안 된다."""
        return self._valid
    
    @property
    def scene_time(self):
        """이 씬이 시작된 뒤 지난 시간 (초). 일시 정지 상태일 때는 올라가지 않는다."""
        return self._scene_time


    def remove(self):
        """이 Scene을 삭제하도록 요청한다. 실제 삭제는 나중 프레임에서 이루어진다."""
        self._valid = False

    # 아래는 자식 클래스에서 덮어쓸 함수 #

    def update(self):
        """Scene을 업데이트한다."""
        pass

    def draw(self, surface: Surface):
        """Scene을 화면에 그린다."""
        pass

    def on_destroy(self):
        """Scene이 삭제되기 전 호출된다. 필요하다면 사용한 리소스를 반환한다. 직접 호출해서는 안 된다!"""
        pass
