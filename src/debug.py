import pygame
from fonts import Fonts
from typing import TYPE_CHECKING, Tuple, Union
from constants import DEBUG_MODE, DEBUG_DRAW_HITBOX
import game_globals

if TYPE_CHECKING:
    global _point_like
    _point_like = Union[Tuple[float, float], pygame.Vector2]

_draws = {
    "line": [],
    "point": [],
    "rect": [],
}

def draw_debug_elements(surface: "pygame.Surface"):
    if not DEBUG_MODE:
        return

    for text, color, p1, p2 in _draws["line"]:
        pm = ((p1[0] + p2[0]) / 2, (p1[1] + p2[0]) / 2 - 10)
        pygame.draw.line(surface, color, p1, p2, 2)
        Fonts.get("debug").render_to(
            surface,
            pm,
            text,
            color
        )
    _draws["line"].clear()

    for text, color, p1 in _draws["point"]:
        pm = (p1[0] + 5, p1[1] - 15)
        pygame.draw.circle(surface, (0, 0, 0, 100), p1, 4.0)
        pygame.draw.circle(surface, color, p1, 2.0)
        Fonts.get("debug").render_to(
            surface,
            pm,
            text,
            color,
            (0, 0, 0, 150)
        )
    _draws["point"].clear()

    for text, color, rect in _draws["rect"]:
        pm = (rect.left, rect.top - 10)
        pygame.draw.rect(surface, color, rect, 2)
        Fonts.get("debug").render_to(
            surface,
            pm,
            text,
            color
        )
    _draws["rect"].clear()

def draw_line(p1: "_point_like", p2: "_point_like", desc="", color=(0,255,255), on_map=False):
    if on_map:
        p1 = (p1[0] - game_globals.camera_offset.x, p1[1] - game_globals.camera_offset.y)
        p2 = (p2[0] - game_globals.camera_offset.x, p2[1] - game_globals.camera_offset.y)
    _draws["line"].append((desc, color, p1, p2))

def draw_point(p1: "_point_like", desc="", color=(0,255,255), on_map=False):
    if on_map:
        p1 = (p1[0] - game_globals.camera_offset.x, p1[1] - game_globals.camera_offset.y)
    _draws["point"].append((desc, color, p1))

def draw_rect(rect: "pygame.Rect", desc="", color=(0,255,255), on_map=False):
    if on_map:
        rect = rect.move(-game_globals.camera_offset)
    _draws["rect"].append((desc, color, rect))

def draw_vector(origin: "_point_like", vec: "_point_like", desc="", color=(255, 100, 100), on_map=False):
    if on_map:
        origin = (origin[0] - game_globals.camera_offset.x, origin[1] - game_globals.camera_offset.y)
        vec = (vec[0] - game_globals.camera_offset.x, vec[1] - game_globals.camera_offset.y)
    dest = pygame.Vector2(origin[0] + vec[0], origin[1] + vec[1])

    draw_line(origin, dest, "", color)
    draw_point(origin, desc, color)