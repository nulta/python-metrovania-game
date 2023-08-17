from scenes.scene import Scene
from pygame import Surface

class SceneManager():
    _scene_stack: list[Scene] = []

    @classmethod
    def _current_scene(cls) -> (Scene | None):
        stack = cls._scene_stack
        if not stack:
            return None
        else:
            return stack[len(stack) - 1]

    @classmethod
    def update(cls):
        scene = cls._current_scene()
        if scene:
            scene.update()
    
    @classmethod
    def draw(cls, surface: Surface):
        scene = cls._current_scene()
        if scene:
            scene.draw(surface)

    @classmethod
    def push_scene(cls, scene: Scene):
        cls._scene_stack.append(scene)
    
    @classmethod
    def clear_scene(cls):
        cls._scene_stack.clear()