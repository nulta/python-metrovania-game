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
    def load_image(self, resource_name: str, no_alpha: bool = False) -> pygame.Surface:
        """
            이미지 파일을 불러온다.
            주의: load_image를 통해 불러온 이미지에 fill() 등을 하지 말 것!
            필요하다면 불러온 이미지를 copy()한 다음 조작해야 한다.
            왜냐하면, 그렇게 하지 않을 경우 동일한 모든 이미지에 똑같은 변형이 적용되기 때문이다.
        """
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
