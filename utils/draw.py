# Convenience functions such that I dont have to call center_to_topleft every time I want to draw something

import pygame
import numpy as np

from utils.transformations import center_to_topleft


def draw_line(surface, color, start_pos, end_pos, width: int = 1):
    """Apply center_to_topleft() and draw pygame.draw.line."""
    start_pos = center_to_topleft(start_pos)
    end_pos = center_to_topleft(end_pos)
    pygame.draw.line(surface, color, start_pos, end_pos, width)

def draw_lines(surface, color, closed, points, width: int = 1):
    """Apply center_to_topleft() and draw pygame.draw.lines."""
    points = center_to_topleft(points)
    pygame.draw.lines(surface, color, closed, points, width)

def draw_circle(surface,
                color,
                center,
                radius,
                width: int = 0,
                draw_top_right: bool = False,
                draw_top_left: bool = False,
                draw_bottom_left: bool = False,
                draw_bottom_right: bool = False):
    """Apply center_to_topleft() and draw pygame.draw.circle."""
    center = center_to_topleft(center)
    pygame.draw.circle(surface, color, center, radius, width, draw_top_right, draw_top_left, draw_bottom_left, draw_bottom_right)



    


def draw_arrow(surface,
               color,
               end: np.ndarray | tuple | list,
               start: np.ndarray | tuple | list = (0, 0),
               line_width: int = 3,
               head_width: int = 0,
               head_len_perc: float = 0.15, 
               head_len_abs: int | float = 0.25,
               head_wid_perc: float = 0.5,
               head_wid_abs: int | float = None):
    assert type(start) in [np.ndarray, tuple, list], "start must be a numpy array, tuple or list."
    assert type(end) in [np.ndarray, tuple, list], "end must be a numpy array, tuple or list."
    assert type(head_len_perc) in [float, type(None)], "head_len_perc must be a float or None."
    assert type(head_len_abs) in [int, float, type(None)], "head_len_abs must be an integer, float or None."

    start = np.array(start)
    end = np.array(end)

    # calculate the length of the arrow head
    if head_len_abs is not None:
        head_len = head_len_abs
    else:
        head_len = np.linalg.norm(end - start) * head_len_perc

    # calculate the width of the arrow head
    if head_wid_abs is not None:
        head_wid = head_wid_abs
    else:
        head_wid = head_len * head_wid_perc

    # calculate the angle of the vector
    angle = np.arctan2(end[1] - start[1], end[0] - start[0])
    arrow_base = end - np.array([np.cos(angle), np.sin(angle)]) * head_len

    # Normalize the vector to get the perpendicular direction
    dx, dy = end - start
    norm = np.sqrt(dx**2 + dy**2)
    perp_x, perp_y = -dy / norm, dx / norm  # Perpendicular vector
    
    # Compute the left and right points
    left = (arrow_base[0] + head_wid * perp_x, arrow_base[1] + head_wid * perp_y)
    right = (arrow_base[0] - head_wid * perp_x, arrow_base[1] - head_wid * perp_y)
    
    start = center_to_topleft(start)
    end = center_to_topleft(end)
    left = center_to_topleft(left)
    right = center_to_topleft(right)
    arrow_base = center_to_topleft(arrow_base)

    pygame.draw.line(surface, color, start, arrow_base, line_width)
    pygame.draw.polygon(surface, color, (left, end, right), head_width)
