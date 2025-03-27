import pygame
import numpy as np

from settings.settings import WIDTH, HEIGHT, UNIT
from settings.colors import *

from utils.transformations import apply_transformation
from utils.draw import draw_circle, draw_arrow, draw_line, draw_text


class Vector:
    def __init__(self, 
                 x: int | float, 
                 y: int | float, 
                 color: tuple = RED,
                 point_radius: int = 5,
                 point_width: int = 0,
                 line_width: int = 3,
                 head_width: int = 0,
                 head_len_abs: int | float = 0.25,
                 origin: tuple | list | np.ndarray = (0, 0)):
        self.x = x
        self.y = y
        self.x_original = x
        self.y_original = y
        self.color = color
        self.point_radius = point_radius
        self.point_width = point_width
        self.line_width = line_width
        self.head_width = head_width
        self.head_len_abs = head_len_abs
        self.origin = origin
        self.origin_original = origin
    
    def apply_transformation(self, m: np.ndarray | list | tuple, overwrite_original: tuple | list | np.ndarray = None):
        """Applies a transformation matrix to the vector."""
        v = self._select_xy(True) if overwrite_original is None else np.array(overwrite_original)
        self.x, self.y = apply_transformation(v, m)
    
    def draw_as_point(self, surface, color: tuple = None, original: bool = False):
        v = self._select_xy(original)
        color = self._select_color(color)
        draw_circle(surface, color, v, self.point_radius, self.point_width)
    
    def draw_as_arrow(self, surface, color: tuple = None, original: bool = False, overwrite_origin: tuple = None):
        origin = overwrite_origin if overwrite_origin else self.origin
        v = self._select_xy(original) + origin
        color = self._select_color(color)
        draw_arrow(surface, color, v, origin, self.line_width, self.head_width, head_len_abs=self.head_len_abs)
    
    def draw_as_line(self, surface, color: tuple = None, original: bool = False):
        v = self._select_xy(original)
        color = self._select_color(color)
        draw_line(surface, color, self.origin, v, self.line_width)
    
    def draw_span(self, surface, scalar: int = 100, color: tuple = None, original: bool = False):
        v = self._select_xy(original)
        color = self._select_color(color)
        draw_line(surface, color, v*-scalar, v*scalar, self.line_width)
    
    def draw_label(self, surface, font, nudge: tuple = (0.15, 0.1), color: tuple = None, background: tuple = BLACK, original: bool = False, overwrite_text: str = None):
        v = self._select_xy(original)
        vn = v + np.array(nudge)
        color = self._select_color(color)
        text = overwrite_text if overwrite_text else f"[{round(v[0], 2)}, {round(v[1], 2)}]"
        draw_text(surface, font, text, vn, color, background)
    
    def reset(self):
        self.x = self.x_original
        self.y = self.y_original
        self.origin = self.origin_original

    def _select_xy(self, original: bool = False):
        x = self.x_original if original else self.x
        y = self.y_original if original else self.y
        return np.array((x, y))
    
    def _select_color(self, color: tuple = None):
        return self.color if color is None else color
