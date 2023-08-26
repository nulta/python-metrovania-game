from pygame import mixer as mixer
from resource_loader import ResourceLoader

class Audio:
    """사운드를 재생한다."""
    @classmethod
    def play(cls, filename: str):
        resource_path = ResourceLoader.get_resource_path("sounds/" + filename)
        mixer.Sound(resource_path).play()

    class common:
        """흔히 사용되는, 미리 지정된 사운드를 재생한다."""
        @classmethod
        def confirm(cls):
            Audio.play("sfx_confirm.ogg")

        @classmethod
        def select(cls):
            Audio.play("sfx_select.ogg")
