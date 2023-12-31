import pygame
from resource_loader import ResourceLoader
import game_globals
from .scene import Scene
from entity_manager import EntityManager
from entities import Player
from constants import *
from fonts import Fonts
from level import Level
from audio import Audio
from input_manager import InputManager

class GameScene(Scene):
    """GameScene은 인게임 씬이다."""

    def __init__(self, level: Level):
        super().__init__()
        self._level = level
        self._background = self._level._background
        self._foreground = self._level._foreground
        self._tilemap_surface = level.get_tilemap_surface()

        # 음악 재생
        Audio.music_set(level.music)

        self.initialize_level()
    
    def initialize_level(self):
        """스테이지를 깨끗하게 초기화한다!"""
        self._scene_time = 0.0

        # 엔티티 초기화
        EntityManager.initialize(self._level, self)
        self._level.create_entities()


    def update(self):
        EntityManager.update()
        if InputManager.pressed(ACTION_RELOAD_MAP):
            Audio.common.confirm()
            self.initialize_level()

    def draw(self, surface: pygame.Surface):
        camera_pos = game_globals.camera_offset

        # Background
        surface.blit(self._background, (0, 0))

        # Tilemap
        surface.blit(self._tilemap_surface, -camera_pos)

        # Entity
        EntityManager.draw(surface, camera_pos)

        # Foreground
        surface.blit(self._foreground, (0, 0))

        # UI
        self.draw_hp(surface)
        self.draw_boss_hp(surface)

    def draw_hp(self,surface: pygame.Surface):
        from entity_manager import EntityManager
        player = EntityManager.get_player()
        if not player: return  
        hp = player.hp
        mhp = player._max_hp
        pygame.draw.rect(surface, (0, 0, 0),[35,35,210,34])
        pygame.draw.rect(surface, (168, 28, 7),[40,39,hp * (200 / mhp),26])
        text = f"hp:{hp}"
        font_size = 20
        color = (255, 255, 255)

        Fonts.get("bold").render_to(
            surface,
            (44,43),
            text,
            fgcolor=color,
            size=font_size,
        )

    def draw_boss_hp(self,surface: pygame.Surface):
        from entity_manager import EntityManager
        boss = EntityManager.get_boss()
        if not boss: return  
        hp = boss.hp
        mhp = boss._max_hp

        base_offset = 600
        pygame.draw.rect(surface, (0, 0, 0),[base_offset,35,210,34])
        pygame.draw.rect(surface, (7, 28, 168),[base_offset+5,39,hp * (200 / mhp),26])
        text = f"hp:{hp}"
        font_size = 20
        color = (255, 255, 255)

        Fonts.get("bold").render_to(
            surface,
            (base_offset+10,43),
            text,
            fgcolor=color,
            size=font_size,
        )

    def on_destroy(self):
        pass
    
    def victory(self):
        """맵을 클리어한다. 잠시 뒤에 다음 씬으로 이동한다."""
        from scene_manager import SceneManager
        from resource_loader import ResourceLoader
        assert self._level.next_scene_name
        
        # 전부 소문자라면 스테이지 이름, 아니라면 씬 이름.
        next_name = self._level.next_scene_name
        if next_name.lower() == next_name:
            # 소문자 -> 스테이지 이름 -> GameScene
            SceneManager.clear_scene()
            leveldata = ResourceLoader.load_level_data(next_name)
            level = Level(leveldata)
            scene = GameScene(level)
            SceneManager.push_scene(scene)
        else:
            # 대문자 포함 -> 
            from . import story_scene
            scene = getattr(story_scene, next_name)
            assert issubclass(scene, Scene)

            SceneManager.clear_scene()
            SceneManager.push_scene(scene())

            
