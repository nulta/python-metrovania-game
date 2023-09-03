import pygame
from fonts import Fonts
from typing import TYPE_CHECKING, Tuple, Union

if TYPE_CHECKING:
    global _point_like
    _point_like = Union[Tuple[int | float, int | float], pygame.Vector2]

_draws = {
    "line": [],
    "point": [],
    "rect": [],
}

def _draw(surface: "pygame.Surface"):
    if not __debug__:
        return

    for x in _draws["line"]:
        text = x[0]
        color = x[1]
        p1 = x[2]
        p2 = x[3]
        pm = ((p1[0] + p2[0]) / 2, (p1[1] + p2[0]) / 2 - 10)
        pygame.draw.line(surface, color, p1, p2, 2)
        Fonts.get("debug").render_to(
            surface,
            pm,
            text,
            color
        )
    _draws["line"].clear()

    for x in _draws["point"]:
        text = x[0]
        color = x[1]
        p1 = x[2]
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

    for x in _draws["rect"]:
        text = x[0]
        color = x[1]
        rect: "pygame.Rect" = x[2]
        pm = (rect.left, rect.top - 10)
        pygame.draw.rect(surface, color, rect, 2)
        Fonts.get("debug").render_to(
            surface,
            pm,
            text,
            color
        )
    _draws["rect"].clear()

def draw_line(p1: "_point_like", p2: "_point_like", desc="", color=(0,255,255)):
    _draws["line"].append((desc, color, p1, p2))

def draw_point(p1: "_point_like", desc="", color=(0,255,255)):
    _draws["point"].append((desc, color, p1))

def draw_rect(rect: "pygame.Rect", desc="", color=(0,255,255)):
    _draws["rect"].append((desc, color, rect))

def draw_vector(origin: "_point_like", vec: "_point_like", desc="", color=(255, 100, 100)):
    dest = pygame.Vector2(origin[0] + vec[0], origin[1] + vec[1])

    draw_line(origin, dest, "", color)
    draw_point(origin, desc, color)