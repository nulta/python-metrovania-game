from constants import *
import pygame
from os import path

class ResourceLoader():
    """
        게임 내의 모든 리소스를 불러오는 도우미 클래스.
        리소스를 전체 경로가 아닌 이름으로 불러올 수 있게 한다.
        최적화를 위해, 불러온 리소스를 캐싱한다.
    """

    _resource_root = path.realpath(RESOURCE_PATH)
    _resource_cache = {}

    @classmethod
    def get_resource_path(cls, resource_name: str) -> str:
        resource_name = resource_name.lower().strip()
        resource_path = path.join(cls._resource_root, resource_name)
        resource_path = path.realpath(resource_path)
        return resource_path

    @classmethod
    def _cache(cls, resource_name, resource):
        resource_name = resource_name.lower()
        cls._resource_cache[resource_name] = resource

    @classmethod
    def _get_cache(cls, resource_name):
        resource_name = resource_name.lower()
        return cls._resource_cache.get(resource_name, None)

    @classmethod
    def _clear_cache(cls):
        cls._resource_cache.clear()


    @classmethod
    def load_image(cls, resource_name: str, no_alpha: bool = False) -> pygame.Surface:
        """이미지 파일을 불러온다.

        주의: load_image를 통해 불러온 이미지에 fill() 등을 하지 말 것!
        필요하다면 불러온 이미지를 copy() 함수로 복사한 다음 조작해야 한다.
        """
        # 같은 리소스를 두 번 로딩하지 않는다
        cache = cls._get_cache(resource_name)
        if cache: return cache

        resource_path = cls.get_resource_path(resource_name)
        surface = pygame.image.load(resource_path)
        if no_alpha:
            surface = surface.convert()
        else:
            surface = surface.convert_alpha()

        cls._cache(resource_name, surface)
        return surface

    @classmethod
    def load_image_2x(cls, resource_name: str, no_alpha: bool = False) -> pygame.Surface:
        """이미지 파일을 2배로 확대해서 불러온다.

        주의: load_image를 통해 불러온 이미지에 fill() 등을 하지 말 것!
        필요하다면 불러온 이미지를 copy() 함수로 복사한 다음 조작해야 한다.
        """
        # 같은 리소스를 두 번 로딩하지 않는다
        cache_name = resource_name + "$2x"
        cache = cls._get_cache(cache_name)
        if cache: return cache

        surface = cls.load_image(resource_name, no_alpha)
        w, h = surface.get_size()
        surface = pygame.transform.scale(surface, (w*2, h*2))

        cls._cache(cache_name, surface)
        return surface
