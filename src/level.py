from typing import Sequence
import pygame

class Level:
    def __init__(self, map_data: "Sequence[Sequence[int | None]]"):
        self._map_data = map_data
    
    
