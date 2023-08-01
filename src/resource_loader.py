from constants import *
import pygame
from os import path

class ResourceLoader():
    """
        게임 내의 모든 리소스를 불러오는 도우미 클래스.
        리소스를 전체 경로가 아닌 이름으로 불러올 수 있게 한다.
        최적화를 위해, 불러온 리소스를 캐싱한다.
    """
    
    _resource_root = RESOURCE_PATH
    _resource_cache = {}

    @classmethod
    def _cache(self, resource_name, resource):
        resource_name = resource_name.lower()
        self._resource_cache[resource_name] = resource
    
    @classmethod
    def _get_cache(self, resource_name):
        resource_name = resource_name.lower()
        return self._resource_cache.get(resource_name, None)

    @classmethod
    def _clear_cache(self):
        self._resource_cache.clear()


    @classmethod
    def load_image(self, resource_name: str, no_alpha: bool = False):
        """이미지 파일을 불러온다."""
        # 같은 리소스를 두 번 로딩하지 않는다
        cache = self._get_cache(resource_name)
        if cache: return cache

        resource_name = resource_name.lower()
        resource_path = path.join(self._resource_root, resource_name)
        surface = pygame.image.load(resource_path)
        if no_alpha:
            surface = surface.convert()
        else:
            surface = surface.convert_alpha()

        self._cache(resource_name, surface)
        return surface

