import pygame
import numpy as np

from settings.settings import WIDTH, HEIGHT, UNIT
from settings.colors import *

from utils.transformations import apply_transformation
from utils.draw import draw_circle, draw_arrow, draw_line


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
    
    def apply_transformation(self, m: np.ndarray | list | tuple, original: bool = True):
        """Applies a transformation matrix to the vector."""
        v = self._select_xy(original)
        self.x, self.y = apply_transformation(v, m)
    
    def draw_as_point(self, surface, color: tuple = None, original: bool = False):
        v = self._select_xy(original)
        if color is None:
            color = self.color
        draw_circle(surface, color, v, self.point_radius, self.point_width)
    
    def draw_as_arrow(self, surface, color: tuple = None, original: bool = False):
        v = self._select_xy(original)
        if color is None:
            color = self.color
        draw_arrow(surface, color, v, self.origin, self.line_width, self.head_width, head_len_abs=self.head_len_abs)
    
    def draw_as_line(self, surface, color: tuple = None, original: bool = False):
        v = self._select_xy(original)
        if color is None:
            color = self.color
        draw_line(surface, color, self.origin, v, self.line_width)
    
    def draw_span(self, surface, scalar: int = 100, color: tuple = None, original: bool = False):
        v = self._select_xy(original)
        if color is None:
            color = self.color
        draw_line(surface, color, v*-scalar, v*scalar, self.line_width)
        

    def _select_xy(self, original: bool = False):
        x = self.x_original if original else self.x
        y = self.y_original if original else self.y
        return np.array((x, y))
