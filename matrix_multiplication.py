import pygame
import pygame_gui
import numpy as np
import textwrap

import pygame_gui.elements.ui_button

from settings.settings import WIDTH, HEIGHT, UNIT
from settings.colors import *
from utils.transformations import center_to_topleft, apply_transformation, get_matrices_for_smooth_transformation, topleft_to_center
from objects.coordinate_system import CoordinateSystem2D
from objects.vector import Vector
from objects.textbox import Textbox
from utils.draw import draw_lines, draw_text








# Plan for this one:
# 1. Vectors as points and arrows
    # Start with label and point of single datum 
# 2. Unit Vectors i-hat and j-hat
# 3. Span of a vector 
# 4. Matrix multiplications as transforming the coordinate system (instructions where i-hat and j-hat land)
# 5. Inverse of a matrix to transform back
# 6. Dimensionality reduction with matrix multiplication, cant go back with inverse


# Initialize pygame
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont(None, 24)
running = True  






# Initialize gui manager
manager = pygame_gui.UIManager((WIDTH, HEIGHT))
playground_manager = pygame_gui.UIManager((WIDTH, HEIGHT))
dropdown = pygame_gui.elements.UIDropDownMenu(
    options_list=["What is a Vector?", "Unit Vectors", "Matrix Multiplication", "Inverse of a matrix", "Dimensionality reduction", "Matrices with no inverse", "Playground"],
    starting_option="What is a Vector?",
    relative_rect=pygame.Rect(center_to_topleft((-4.5, 4.5)), (UNIT*2, UNIT*0.5)),
    manager=manager
)

def set_visualize_true():
    global visualize
    visualize = not visualize

visualize_button = pygame_gui.elements.UIButton(
    text = "visualize",
    relative_rect=pygame.Rect(center_to_topleft((-2.5, 4.5)), (UNIT*2, UNIT*0.5)),
    manager=manager,
    command=set_visualize_true
)

m_a_input = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect(center_to_topleft((-4.3, 4)), (UNIT, UNIT*0.5)),
    manager=playground_manager,
    placeholder_text="m_a",
    object_id="#m_a_input",
    initial_text="1"
)
m_b_input = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect(center_to_topleft((-3.3, 4)), (UNIT, UNIT*0.5)),
    manager=playground_manager,
    placeholder_text="m_b",
    object_id="#m_b_input",
    initial_text="0"
)
m_c_input = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect(center_to_topleft((-4.3, 3.5)), (UNIT, UNIT*0.5)),
    manager=playground_manager,
    placeholder_text="m_c",
    object_id="#m_c_input",
    initial_text="0"
)
m_d_input = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect(center_to_topleft((-3.3, 3.5)), (UNIT, UNIT*0.5)),
    manager=playground_manager,
    placeholder_text="m_d",
    object_id="#m_d_input",
    initial_text="1"
)

# Objects
coordinate_system = CoordinateSystem2D(-20, 20)
ihat = Vector(1, 0, RED)
jhat = Vector(0, 1, GREEN)
a = Vector(1, 2, ORANGE)
b = Vector(2, 3, ORANGE)
c = Vector(0.7, 0.5, ORANGE)


# text_box
def draw_textbox_background(surface, pos = (-4.5, 4.5), width = 4, height = 4, color = WHITE):
    pygame.draw.rect(surface, color, (center_to_topleft(pos), (UNIT*width, UNIT*height)))

# Text Vector
def draw_text_from_file(file_path, start_pos = (-4.3, 4.3), wrap_width = 40):
    with open(file_path, "r") as f:
        lines = f.readlines()
    for line in lines:
        line = line.replace("\n", "")
        wrapped_line = textwrap.wrap(line, width=wrap_width)
        if wrapped_line == []:
            wrapped_line = [""]
        indent = ""
        if line.startswith("    - "):
            indent = "      "
        for i, l in enumerate(wrapped_line):
            if i > 0:
                l = textwrap.indent(l.replace("\n", ""), indent)
            draw_text(screen, font, l.replace("\n", "").replace("\t", "   "), start_pos)
            start_pos = (start_pos[0], start_pos[1] + -0.25)


# What is a vector?
def what_is_a_vector(visualize=False):
    # Coordinate system
    screen.fill(BLACK)
    coordinate_system.draw(screen, which_grid="")

    # Text box
    draw_textbox_background(screen)
    draw_text_from_file("content/what_is_a_vector.txt")

    # Draw a
    a.draw_as_point(screen)
    a.draw_label(screen, font, nudge=(0.1, 0.25))

    if visualize:
        # Coordinate system
        screen.fill(BLACK)
        coordinate_system.draw(screen, which_grid="")

        # Text box
        draw_textbox_background(screen)
        draw_text_from_file("content/what_is_a_vector.txt")

        # Draw random points
        x = np.random.randint(-4, 4, 10)
        y = np.random.randint(-4, 4, 10)
        vs = [Vector(x[i], y[i], ORANGE) for i in range(10)]
        
        for v in vs: 
            v.draw_as_point(screen)
            v.draw_label(screen, font, nudge=(0.1, 0.25))
            manager.draw_ui(screen)
            manager.update(time_delta)
            pygame.display.flip()
            pygame.time.wait(200)
        
        for v in vs: 
            [v.draw_as_point(screen) for v in vs]
            v.draw_as_arrow(screen)
            [v.draw_label(screen, font, nudge=(0.1, 0.25)) for v in vs]
            manager.draw_ui(screen)
            manager.update(time_delta)
            pygame.display.flip()
            pygame.time.wait(200)

# Unit Vectors
def unit_vectors(visualize=False):
    # Coordinate system
    screen.fill(BLACK)
    coordinate_system.draw(screen, which_grid="xy")

    # Text box
    draw_textbox_background(screen)
    draw_text_from_file("content/unit_vectors.txt")

    # Draw i-hat
    ihat.reset()
    ihat.draw_as_arrow(screen)
    ihat.draw_label(screen, font)

    # Draw j-hat
    jhat.reset()
    jhat.draw_as_arrow(screen)
    jhat.draw_label(screen, font)

    if visualize:
        # Reset i-hat and j-hat
        ihat.reset()
        jhat.reset()

        # Get new vector with target coordinates
        v = Vector(1, 1, ORANGE)

        # Get matrices for smooth transformation
        smooth_m_ihat = get_matrices_for_smooth_transformation(((np.random.randint(-4, 4, 1)[0], 0), (0, 1)))
        smooth_m_jhat = get_matrices_for_smooth_transformation(((1, 0), (0, np.random.randint(-4, 4, 1)[0])))

        # Shift j-hat to the right
        for x in np.linspace(0, 1, 50):
            # Coordinate system
            screen.fill(BLACK)
            coordinate_system.draw(screen, which_grid="")

            # Text box
            draw_textbox_background(screen)
            draw_text_from_file("content/unit_vectors.txt")

            # Draw b
            v.draw_as_point(screen)
            v.draw_label(screen, font)

            # draw unit vectors
            jhat.origin = (x, 0)
            jhat.draw_as_arrow(screen)
            jhat.draw_label(screen, font)
            ihat.draw_as_arrow(screen)
            ihat.draw_label(screen, font)

            # UI and flip
            manager.draw_ui(screen)
            manager.update(time_delta)
            pygame.display.flip()
            pygame.time.wait(50)
        pygame.time.wait(1000)

        # Scale i-hat and j-hat to move v to target
        for smi, smj in zip(smooth_m_ihat, smooth_m_jhat):
            # Coordinate system
            screen.fill(BLACK)
            coordinate_system.draw(screen, which_grid="")

            # Text box
            draw_textbox_background(screen)
            draw_text_from_file("content/unit_vectors.txt")

            # Transform i-hat and j-hat
            ihat.apply_transformation(smi)
            jhat.apply_transformation(smj)
            jhat.origin = apply_transformation((1, 0), smi)

            # Update v position
            v.x = ihat.x
            v.y = jhat.y

            # Draw vectors
            ihat.draw_as_arrow(screen)
            ihat.draw_label(screen, font)

            jhat.draw_as_arrow(screen)
            jhat.draw_label(screen, font)

            v.draw_as_point(screen)
            v.draw_label(screen, font)

            # UI and flip
            manager.draw_ui(screen)
            manager.update(time_delta)
            pygame.display.flip()
            pygame.display.update()
            pygame.time.wait(50)
        pygame.time.wait(2000)

# matrix multiplication
def matrix_multiplication(visualize=False):
    # Coordinate system
    screen.fill(BLACK)
    coordinate_system.generate()
    coordinate_system.draw(screen, which_grid="xy")

    # Text box
    draw_textbox_background(screen)
    draw_text_from_file("content/matrix_multiplication.txt")

    # Draw i-hat
    ihat.reset()
    ihat.draw_as_arrow(screen)
    ihat.draw_label(screen, font)

    # Draw j-hat
    jhat.reset()
    jhat.draw_as_arrow(screen)
    jhat.draw_label(screen, font)

    if visualize:
        # Draw random points
        x = np.random.normal(0, 1, 2).tolist() + [1]
        y = np.random.normal(0, 1, 2).tolist() + [1]
        xys = np.round(np.array((x, y)).T, 2)
        vs = [Vector(x[i], y[i], ORANGE) for i in range(len(x))]
        m = np.array((np.random.randint(-2, 2, 2), np.random.randint(-2, 2, 2)))
        smooth_m = get_matrices_for_smooth_transformation(m)

        # Text box
        draw_text(screen, font, f"{str(xys)}", (-4.3, 4))
        draw_text(screen, font, f"x", (-3.1, 3.8))
        draw_text(screen, font, f"{str(m)}", (-2.9, 3.9))
        
        for v in vs: 
            v.draw_as_point(screen)
            manager.draw_ui(screen)
            manager.update(time_delta)
            pygame.display.flip()
            pygame.time.wait(200)
        
        for sm in smooth_m:
            # Coordinate system
            screen.fill(BLACK)
            coordinate_system.apply_transformation(sm)
            coordinate_system.draw(screen)

            # Text box
            draw_textbox_background(screen)
            draw_text(screen, font, f"{str(xys)}", (-4.3, 4))
            draw_text(screen, font, f"x", (-3.1, 3.8))
            draw_text(screen, font, f"{str(np.round(sm, 2))}", (-2.9, 3.9))
            draw_text(screen, font, f"=", (-3.1, 2.9))
            draw_text(screen, font, f"{str(np.round(apply_transformation(xys, sm), 2))}", (-2.9, 3))
            
            # Draw vectors
            [v.apply_transformation(sm) for v in vs]
            [v.draw_as_point(screen) for v in vs]
            [v.draw_as_arrow(screen) for v in vs]

            # Transform i-hat and j-hat
            ihat.apply_transformation(sm)
            jhat.apply_transformation(sm)

            # Draw vectors
            ihat.draw_as_arrow(screen)
            ihat.draw_label(screen, font)
            jhat.draw_as_arrow(screen)
            jhat.draw_label(screen, font)

            # UI and flip
            manager.draw_ui(screen)
            manager.update(time_delta)
            pygame.display.flip()
            pygame.time.wait(50)
        pygame.time.wait(5000)

# Inverse of a matrix
def inverse_of_a_matrix(visualize=False):
    # Coordinate system
    screen.fill(BLACK)
    coordinate_system.generate()
    coordinate_system.draw(screen, which_grid="xy")

    # Text box
    draw_textbox_background(screen)
    draw_text_from_file("content/inverse_of_a_matrix.txt")

    # Draw i-hat
    ihat.reset()
    ihat.draw_as_arrow(screen)
    ihat.draw_label(screen, font)

    # Draw j-hat
    jhat.reset()
    jhat.draw_as_arrow(screen)
    jhat.draw_label(screen, font)

    if visualize:
        smooth_m = get_matrices_for_smooth_transformation(((1, 1), (1, 2)))
        for sm in smooth_m:
            # Coordinate system
            screen.fill(BLACK)
            coordinate_system.apply_transformation(sm)
            coordinate_system.draw(screen)

            # Text box
            draw_textbox_background(screen)
            draw_text(screen, font, f"{str(np.array(((1, 0), (0, 1))))}", (-4.3, 4))
            draw_text(screen, font, f"x", (-3.1, 3.8))
            draw_text(screen, font, f"{str(np.round(sm, 2))}", (-2.9, 3.9))
            draw_text(screen, font, f"=", (-3.1, 2.9))
            draw_text(screen, font, f"{str(np.round(apply_transformation(np.array(((1, 0), (0, 1))), sm), 2))}", (-2.9, 3))

            # Transform i-hat and j-hat
            ihat.apply_transformation(sm)
            jhat.apply_transformation(sm)

            # Draw vectors
            ihat.draw_as_arrow(screen)
            ihat.draw_label(screen, font)
            jhat.draw_as_arrow(screen)
            jhat.draw_label(screen, font)

            # UI and flip
            manager.draw_ui(screen)
            manager.update(time_delta)
            pygame.display.flip()
            pygame.time.wait(50)
        pygame.time.wait(3000)

        new_points, new_x_axis, new_y_axis = coordinate_system.points, coordinate_system.x_axis, coordinate_system.y_axis
        new_ihat = (ihat.x, ihat.y)
        new_jhat = (jhat.x, jhat.y)
        smooth_m = get_matrices_for_smooth_transformation(((2, -1), (-1, 1)))
        for sm in smooth_m:
            # Coordinate system
            screen.fill(BLACK)
            coordinate_system.apply_transformation(sm, overwrite_original=(new_points, new_x_axis, new_y_axis))
            coordinate_system.draw(screen)

            # Text box
            draw_textbox_background(screen)
            draw_text(screen, font, f"{str(np.array((new_ihat, new_jhat)))}", (-4.3, 4))
            draw_text(screen, font, f"x", (-3.1, 3.8))
            draw_text(screen, font, f"{str(np.round(sm, 2))}", (-2.9, 3.9))
            draw_text(screen, font, f"=", (-3.1, 2.9))
            draw_text(screen, font, f"{str(np.round(apply_transformation(np.array((new_ihat, new_jhat)), sm), 2))}", (-2.9, 3))

            # Transform i-hat and j-hat
            ihat.apply_transformation(sm, new_ihat)
            jhat.apply_transformation(sm, new_jhat)

            # Draw vectors
            ihat.draw_as_arrow(screen)
            ihat.draw_label(screen, font)
            jhat.draw_as_arrow(screen)
            jhat.draw_label(screen, font)

            # UI and flip
            manager.draw_ui(screen)
            manager.update(time_delta)
            pygame.display.flip()
            pygame.time.wait(50)
        pygame.time.wait(3000)

# Dimensionality reduction
def dimensionality_reduction(visualize=False):
    # Coordinate system
    screen.fill(BLACK)
    coordinate_system.generate()
    coordinate_system.draw(screen, which_grid="xy")

    # Text box
    draw_textbox_background(screen)
    draw_text_from_file("content/dimensionality_reduction.txt")

    # Draw i-hat
    ihat.reset()
    ihat.draw_as_arrow(screen)
    ihat.draw_label(screen, font)

    # Draw j-hat
    jhat.reset()
    jhat.draw_as_arrow(screen)
    jhat.draw_label(screen, font)

    if visualize:
        smooth_m = get_matrices_for_smooth_transformation(((2, 3), (2, 3)))
        x = np.random.normal(0, 1, 10)
        y = np.random.normal(0, 1, 10)
        vs = [Vector(x[i], y[i], ORANGE) for i in range(len(x))]

        for v in vs:
            v.draw_as_point(screen)
            manager.draw_ui(screen)
            manager.update(time_delta)
            pygame.display.flip()
            pygame.time.wait(200)

        for sm in smooth_m:
            # Coordinate system
            screen.fill(BLACK)
            coordinate_system.apply_transformation(sm)
            coordinate_system.draw(screen, which_grid="xy")

            # Text box
            draw_textbox_background(screen)
            draw_text_from_file("content/dimensionality_reduction.txt")

            # Draw i-hat
            ihat.apply_transformation(sm)
            ihat.draw_as_arrow(screen)
            ihat.draw_label(screen, font)

            # Draw j-hat
            jhat.apply_transformation(sm)
            jhat.draw_as_arrow(screen)
            jhat.draw_label(screen, font)

            # Draw vectors
            [v.apply_transformation(sm) for v in vs]
            [v.draw_as_point(screen) for v in vs]

            # UI and flip
            manager.draw_ui(screen)
            manager.update(time_delta)
            pygame.display.flip()
            pygame.time.wait(50)
        pygame.time.wait(3000)

# No inverse
def no_inverse(visualize=False):
    # Coordinate system
    screen.fill(BLACK)
    coordinate_system.generate()
    coordinate_system.draw(screen, which_grid="xy")

    # Text box
    draw_textbox_background(screen)
    draw_text_from_file("content/matrices_with_no_inverse.txt")

    # Draw i-hat
    ihat.reset()
    ihat.draw_as_arrow(screen)
    ihat.draw_label(screen, font)

    # Draw j-hat
    jhat.reset()
    jhat.draw_as_arrow(screen)
    jhat.draw_label(screen, font)
    
    # Define matrix with no inverse
    m = np.array(((1, 0), (0, 0))).T
    smooth_m = get_matrices_for_smooth_transformation(m)

    # Draw two points that land on the same point
    x = Vector(-2, 1, ORANGE)
    y = Vector(-2, -1, PURPLE)
    x.draw_as_point(screen)
    y.draw_as_point(screen)
    x.draw_as_arrow(screen)
    y.draw_as_arrow(screen)
    x.draw_label(screen, font)
    y.draw_label(screen, font)


    if visualize:
        for sm in smooth_m:
            # Coordinate system
            screen.fill(BLACK)
            coordinate_system.apply_transformation(sm)
            coordinate_system.draw(screen, which_grid="xy")

            # Transform i-hat and j-hat
            ihat.apply_transformation(sm)
            jhat.apply_transformation(sm)

            # Draw vectors
            ihat.draw_as_arrow(screen)
            jhat.draw_as_arrow(screen)
            ihat.draw_label(screen, font)
            jhat.draw_label(screen, font)

            # Transform x and y
            x.apply_transformation(sm)
            y.apply_transformation(sm)

            # Draw original positions
            x.draw_as_point(screen, original=True)
            y.draw_as_point(screen, original=True)

            # Draw vectors
            x.draw_as_point(screen)
            x.draw_as_arrow(screen)
            y.draw_as_point(screen)
            y.draw_as_arrow(screen)
            y.draw_label(screen, font)
            x.draw_label(screen, font)

            # Textbox
            draw_text(screen, font, f"(-2, 1) and (2, 1) both land on (-2, 0) after transforming them with A = ((1, 0), (0, 0)).\nTheir dimensionality was reduced from 2D to 1D. \nNow it is impossible to know which of these points should go where\nafter reversing the transformation.\nTherefore the transformation is not invertible (i.e., A has no inverse).", (-4.3, 4))

            # UI and flip
            manager.draw_ui(screen)
            manager.update(time_delta)
            pygame.display.flip()
            pygame.time.wait(50)
        pygame.time.wait(10000)

# Playground
def playground(points=[], visualize=False):
    # Coordinate system
    screen.fill(BLACK)
    coordinate_system.generate()
    coordinate_system.draw(screen, which_grid="xy")

    # Text box
    draw_textbox_background(screen)

    [p.draw_as_point(screen) for p in points]
    [p.draw_label(screen, font, nudge=(0.1, 0.25)) for p in points]

    # Draw i-hat
    ihat.reset()
    ihat.draw_as_arrow(screen)
    ihat.draw_label(screen, font)

    # Draw j-hat
    jhat.reset()
    jhat.draw_as_arrow(screen)
    jhat.draw_label(screen, font)

    # add points by clicking
    if pygame.mouse.get_pressed()[0]:
        pos = pygame.mouse.get_pos()
        # if pos is over the matrix inputs dont add point
        if m_a_input.rect.collidepoint(pos) or m_b_input.rect.collidepoint(pos) or m_c_input.rect.collidepoint(pos) or m_d_input.rect.collidepoint(pos) or dropdown.rect.collidepoint(pos) or visualize_button.rect.collidepoint(pos):
            pass
        else:
            pos = topleft_to_center((pos[0], pos[1]))
            points.append(Vector(pos[0], pos[1], ORANGE))
    
    if visualize:
        m = ((float(m_a_input.get_text()), float(m_b_input.get_text())), (float(m_c_input.get_text()), float(m_d_input.get_text())))
        smooth_m = get_matrices_for_smooth_transformation(m)
        for sm in smooth_m:
            # Coordinate system
            screen.fill(BLACK)
            coordinate_system.apply_transformation(sm)
            coordinate_system.draw(screen, which_grid="xy")
            
            # Draw i-hat
            ihat.apply_transformation(sm)
            ihat.draw_as_arrow(screen)
            ihat.draw_label(screen, font)

            # Draw j-hat
            jhat.apply_transformation(sm)
            jhat.draw_as_arrow(screen)
            jhat.draw_label(screen, font)

            # Text box
            draw_textbox_background(screen)

            [p.apply_transformation(sm) for p in points]
            [p.draw_as_point(screen) for p in points]
            # [p.draw_label(screen, font, nudge=(0.1, 0.25)) for p in points]

            # UI and flip
            manager.draw_ui(screen)
            manager.update(time_delta)
            playground_manager.draw_ui(screen)
            playground_manager.update(time_delta)
            pygame.display.flip()
            pygame.time.wait(50)

        pygame.time.wait(3000)
        points = []
        visualize = False
    
    manager.draw_ui(screen)
    manager.update(time_delta)
    playground_manager.draw_ui(screen)
    playground_manager.update(time_delta)
    pygame.display.flip()




visualize = False
points = []
while running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        manager.process_events(event)
        playground_manager.process_events(event)

        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            visualize = False

        # check if escape key is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                visualize = False

    # What is a vector?
    if dropdown.selected_option[0] == "What is a Vector?":
        what_is_a_vector(visualize)
        
    elif dropdown.selected_option[0] == "Unit Vectors":
        unit_vectors(visualize)

    elif dropdown.selected_option[0] == "Matrix Multiplication":
        matrix_multiplication(visualize)
    
    elif dropdown.selected_option[0] == "Inverse of a matrix":
        inverse_of_a_matrix(visualize)
    
    elif dropdown.selected_option[0] == "Dimensionality reduction":
        dimensionality_reduction(visualize)

    elif dropdown.selected_option[0] == "Matrices with no inverse":
        no_inverse(visualize)

    elif dropdown.selected_option[0] == "Playground":
        playground(points, visualize)

        
        
    manager.draw_ui(screen)
    manager.update(time_delta)
    pygame.display.flip()
    