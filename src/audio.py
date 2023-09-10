from pygame import mixer as mixer
from pygame.mixer import music as music_mixer
from resource_loader import ResourceLoader
from util import clamp

class Audio:
    """사운드를 재생한다."""

    _master_music_volume = 1.0
    _master_sfx_volume = 1.0
    _current_music = ""

    @classmethod
    def get_master_music_volume(cls):
        return cls._master_music_volume

    @classmethod
    def set_master_music_volume(cls, val: "float"):
        cls._master_music_volume = clamp(val, 0, 1)

    @classmethod
    def get_master_sfx_volume(cls):
        return cls._master_sfx_volume

    @classmethod
    def set_master_sfx_volume(cls, val: "float"):
        cls._master_sfx_volume = clamp(val, 0, 1)


    @classmethod
    def play(cls, filename: str):
        """지정된 사운드를 재생한다. 파일명은 자동으로 `sounds/{filename}.ogg` 형식으로 치환된다."""
        resource_path = ResourceLoader.get_resource_path("sounds/" + filename + ".ogg")
        sound = mixer.Sound(resource_path)
        sound.set_volume(cls._master_sfx_volume)
        sound.play()

    @classmethod
    def music_set(cls, music_name: "(str | None)"):
        """현재 음악을 멈추고 지정된 음악을 재생한다. `music_name`이 빈 문자열이나 None이라면 현재 음악을 멈춘다."""
        print("Current music ->", music_name)

        if not music_name:
            music_mixer.unload()
            return
        
        # 같은 음악은 끊지 않는다
        if cls._current_music == music_name:
            return
        cls._current_music = music_name

        music_res = f"sounds/music/{music_name}.ogg"
        music_path = ResourceLoader.get_resource_path(music_res)
        music_mixer.load(music_path)
        cls.music_set_volume(1.0)
        music_mixer.play(-1)

    @classmethod
    def music_set_volume(cls, val: float):
        """현재 음악의 볼륨을 조절한다."""
        music_mixer.set_volume(cls._master_music_volume * val)


    class common:
        """흔히 사용되는, 미리 지정된 사운드를 재생한다."""
        @classmethod
        def confirm(cls):
            Audio.play("sfx_confirm")

        @classmethod
        def select(cls):
            Audio.play("sfx_select")
