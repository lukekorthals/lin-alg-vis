import numpy as np
from typing import Tuple

from utils.transformations import apply_transformation
from utils.draw import draw_lines
from settings.colors import *
from settings.settings import WIDTH, HEIGHT, UNIT

class CoordinateSystem2D:
    def __init__(self, 
                 min: int | float = -10,
                 max: int | float = 10,
                 x_color: tuple = WHITE,
                 y_color: tuple = WHITE,
                 grid_color: tuple = GREY,
                 axes_width: int = 3,
                 grid_width: int = 1,
                 step: int | float = 1):
        self.min = min
        self.max = max
        self.x_color = x_color
        self.y_color = y_color
        self.grid_color = grid_color
        self.axes_width = axes_width
        self.grid_width = grid_width
        self.step = step
        self.generate()
    
    def generate(self):
        """Generates the 2D grid of points and the x and y axes describing the coordinate system."""
        # Generate 2D grid of points
        n = abs(int((self.min - self.max) / self.step)) + 1
        points = np.array(np.meshgrid(np.linspace(self.min, self.max, n), 
                                      np.linspace(self.min, self.max, n)))
        # Extract x and y axes
        y_axis = points.T[n//2]
        x_axis = points[:, n//2].T

        # Set the attributes
        self.points = points
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.points_original = points
        self.x_axis_original = x_axis
        self.y_axis_original = y_axis

    def apply_transformation(self, m: np.ndarray | tuple | list, overwrite_original: tuple = None):
        """Applies a transformation matrix to the coordinate system."""
        points, x_axis, y_axis = self._select_points(True) if overwrite_original is None else overwrite_original

        self.points = apply_transformation(points.T.reshape(-1, 2), m).T.reshape(points.shape)
        self.x_axis = apply_transformation(x_axis, m)
        self.y_axis = apply_transformation(y_axis, m)
    
    def draw_axes(self, surface, which: str = "xy", original: bool = False):
        """Draws one or both axes of the coordinate system."""
        assert which in ["xy", "x", "y", ""], "which must be one of ['xy', 'x', 'y', '']"
        points, x_axis, y_axis = self._select_points(original)
        if "x" in which:
            draw_lines(surface, self.x_color, False, x_axis, self.axes_width)
        if "y" in which:
            draw_lines(surface, self.y_color, False, y_axis, self.axes_width)
    
    def draw_grid(self, surface, which: str = "xy", original: bool = False):
        """Draws the the grid for one or both axes of the coordinate system."""
        assert which in ["xy", "x", "y", ""], "which must be one of ['xy', 'x', 'y', '']"
        points, x_axis, y_axis = self._select_points(original)
        
        for i in range(points.shape[1]):
            col = points.T[i]
            row = points[:, i].T
            if "x" in which:
                draw_lines(surface, self.grid_color, False, row, self.grid_width)
            if "y" in which:
                draw_lines(surface, self.grid_color, False, col, self.grid_width)
    
    def draw(self, 
             surface, 
             which_axes: str = "xy", 
             which_grid: str = "xy",
             axes_original: bool = False,
             grid_original: bool = False):
        """Draws the coordinate system."""
        self.draw_grid(surface, which_grid, grid_original)
        self.draw_axes(surface, which_axes, axes_original)
    
    def _select_points(self, original: bool = False) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Returns the original or current points, x and y axes."""
        points = self.points_original.copy() if original else self.points.copy()
        x_axis = self.x_axis_original.copy() if original else self.x_axis.copy()
        y_axis = self.y_axis_original.copy() if original else self.y_axis.copy()
        return points, x_axis, y_axis