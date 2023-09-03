from scenes.scene import Scene
from pygame import Surface
from typing import Optional
from util import classproperty
import game_globals

class SceneManager():
    """Scene들을 관리한다.

    SceneManager는 Scene을 '스택 형식'으로 관리한다.
    이는 즉, 한 Scene '위에' 다른 Scene을 올릴 수 있다는 뜻이다.
    이를테면, 게임 Scene 위에 일시정지 메뉴 Scene을 올릴 수 있다.
    이 경우에는, 맨 위에 올라간 씬 (위의 예시에서는 '일시정지 메뉴 Scene')만 업데이트된다.
    """

    _scene_stack: "list[Scene]" = []

    @classproperty
    def current_scene(cls) -> Optional[Scene]:
        stack = cls._scene_stack
        if not stack:
            return None
        else:
            return stack[-1]

    @classproperty
    def scene_time(cls) -> float:
        scene = cls.current_scene
        if scene:
            return scene.scene_time
        else:
            return 0.0

    @classmethod
    def update(cls) -> bool:
        "Scene을 업데이트한다. 업데이트할 Scene이 없을 경우 false를 반환한다."
        scene = cls.current_scene
        if not scene:
            return False

        # 제거 요청된 Scene일 경우
        if not scene._valid:
            scene.on_destroy()
            cls._scene_stack.pop()
            return cls.update()

        scene.update()
        scene._scene_time += game_globals.delta_time
        return True

    @classmethod
    def draw(cls, surface: Surface):
        # 맨 아래에 있는 씬부터 순서대로 그린다
        for scene in cls._scene_stack:
        
            if not scene._valid:
                continue
            scene.draw(surface)

    @classmethod
    def push_scene(cls, scene: Scene):
        cls._scene_stack.append(scene)

    @classmethod
    def clear_scene(cls):
        for scene in reversed(cls._scene_stack):
            scene.on_destroy()
        cls._scene_stack.clear()
