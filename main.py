import pygame
import numpy as np

from settings.settings import WIDTH, HEIGHT, UNIT
from settings.colors import *
from utils.transformations import center_to_topleft, apply_transformation, get_matrices_for_smooth_transformation
from objects.coordinate_system import CoordinateSystem2D
from objects.vector import Vector
from utils.draw import draw_lines


# Initialize coordinate system
coordinate_system = CoordinateSystem2D(-20, 20)

# Initialize data
np.random.seed(0)
x = np.random.normal(0, 1, 100)
y = np.random.normal(0, 1, 100) + x * 0.5
# center the data
x = x - np.mean(x)
y = y - np.mean(y)
data = np.vstack((x, y)).T
vectors = [Vector(v[0], v[1], RED) for v in data]


# Get the eigenvectors of the data
eigenvalues, eigenvectors = np.linalg.eig(np.cov(data.T))
sorted_indices = np.argsort(eigenvalues)[::-1]  # Sort eigenvalues in descending order
largest_eigen_vector = eigenvectors[:, sorted_indices[0]]  # Select the eigenvector corresponding to the largest eigenvalue

m = np.outer(largest_eigen_vector, largest_eigen_vector)
pc1 = Vector(largest_eigen_vector[0], largest_eigen_vector[1], GREEN)
pc2 = Vector(eigenvectors[0, sorted_indices[1]], eigenvectors[1, sorted_indices[1]], ORANGE)
smooth_m = get_matrices_for_smooth_transformation(m, steps=100)
transform = False

# Initialize game
screen = pygame.display.set_mode((WIDTH, HEIGHT))
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw everything
    screen.fill(BLACK)
    coordinate_system.draw(screen)
    # coordinate_system.draw(screen, which_axes="", grid_original=True)
    for v in vectors:
        v.draw_as_point(screen)
    
    pc1.draw_span(screen)
    pc2.draw_span(screen)

    # Start transform when clicking a button on the screen
    if not transform and pygame.mouse.get_pressed()[0]:
        transform = True
    
    
    if transform:
        for sm in smooth_m:
            screen.fill(BLACK)
            # Draw the coordinate system
            coordinate_system.apply_transformation(sm)
            coordinate_system.draw(screen)

            pc1.draw_span(screen)
            pc2.draw_span(screen)
            
            # Draw the data
            for v in vectors:
                v.apply_transformation(sm)
                v.draw_as_point(screen)
                # v.draw_as_arrow(screen)

            pygame.display.update()
            pygame.time.delay(100)
        transform = False

    # for sm in smooth_m:
    #     screen.fill(BLACK)
    #     coordinate_system.apply_transformation(sm)
    #     coordinate_system.draw(screen)
    #     v.apply_transformation(sm)
    #     v.draw_as_point(screen)
    #     v.draw_as_point(screen, BLUE, original=True)
    #     v.draw_as_arrow(screen)

    #     pygame.display.update()
    #     pygame.time.delay(100)


    # # Coordinate axes
    # pygame.draw.lines(screen, WHITE, False, center_to_topleft(x_axis), 2)
    # pygame.draw.lines(screen, WHITE, False, center_to_topleft(y_axis), 2)
    
    # # Some vector
    # for sm in smooth_m:
    #     screen.fill(BLACK)

    #     # Coordinate axes
    #     pygame.draw.lines(screen, WHITE, False, center_to_topleft(x_axis), 2)
    #     pygame.draw.lines(screen, WHITE, False, center_to_topleft(y_axis), 2)

    #     pygame.draw.circle(screen, RED, center_to_topleft(apply_transformation(v, sm)), 5)

    #     pygame.display.update()
    #     pygame.time.delay(100)
    
    pygame.display.update()
