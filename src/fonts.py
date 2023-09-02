import pygame
import pygame.freetype as freetype
from resource_loader import ResourceLoader
from typing import TYPE_CHECKING, Union, Literal

if TYPE_CHECKING:
    global SupportedFonts
    # 사용 가능한 폰트 목록 (타입)
    SupportedFonts = Union[
        Literal["default"],
        Literal["bold"],
        Literal["debug"],
    ]


def _get_font(filename):
    return freetype.Font(
        ResourceLoader.get_resource_path("fonts/" + filename),
        16,
    )

class Fonts():
    _fonts: "dict[SupportedFonts, freetype.Font]" = {}
    _font_names: "dict[SupportedFonts, str]" = {
        "default": "ibmplexsanskr.otf",
        "bold": "ibmplexsanskr_semibold.otf",
        "debug": "ibmplexsanskr.otf",
    }


    @classmethod
    def get(cls, name: "SupportedFonts"):
        if not name in cls._font_names:
            print(f"Fonts.get(): Got invalid font name '{name}'")
            name = "default"
        
        if not name in cls._fonts:
            # Lazy initialization
            cls._fonts[name] = cls._new(name)

        return cls._fonts[name]

    @classmethod
    def _new(cls, name: "SupportedFonts"):
        if not name in cls._font_names:
            print(f"Fonts.new(): Got invalid font name '{name}'")
            name = "default"

        return _get_font(cls._font_names[name])
