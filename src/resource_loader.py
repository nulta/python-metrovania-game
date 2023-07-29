from constants import *
import pygame
from os import path

class ResourceLoader():
    """게임 내의 모든 리소스를 불러오는 도우미 클래스."""
    
    resource_root = RESOURCE_PATH
    
    def load_image(self, resource_name: str):
        resource_name = resource_name.lower()
        resource_path = path.join(self.resource_root, resource_name)
        surface = pygame.image.load(resource_path)
        return surface.convert_alpha()
    