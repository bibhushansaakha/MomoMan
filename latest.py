import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import random
import heapq
import math
import time

# Initialize pygame and OpenGL
pygame.init()
display = (800, 800)  # Display size
pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)
gluOrtho2D(0, display[0], 0, display[1])

# Constants
GRID_SIZE = 20  # Adjusted grid size to fit new window size
CELL_SIZE = display[0] // GRID_SIZE  # Adjust cell size dynamically based on grid size and display width
WALL_WIDTH = 2
BOTTOM_OFFSET = 0

# Colors
MOMOMAN_COLOR = (1, 1, 1)  # White
POINT_COLOR = (1, 0, 0)  # Bright Red
FOOTER_COLOR = (0.2, 0.2, 0.2)  # Dark Gray
WALL_COLOR = (1, 0.5, 0)  # Orange
WALL_COLOR_BRIGHT = (1, 0.75, 0)  # Brighter Orange
WALL_COLOR_YELLOW = (1, 1, 0)  # Yellow
BACKGROUND_COLOR = (0.2, 0.1, 0.1)  # Darker slightly bluish hue
CHEF_COLOR = (0.2, 0.6, 0.4)

# Speed and randomness settings
MOMOMAN_SPEED = 90  # milliseconds per move
CHEF_SPEED = 250  # milliseconds per move
CHEF_RANDOMNESS_LOW = 0.2  # low randomness for some chefs
CHEF_RANDOMNESS_HIGH = 0.8  # high randomness for other chefs

grid_layout = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 2, 2, 2, 2, 0, 3, 0, 3, 0, 0, 2, 2, 2, 2, 0, 1, 0, 1],
    [1, 0, 2, 'X', 'X', 2, 0, 3, 0, 3, 0, 0, 2, 'X', 'X', 2, 0, 1, 0, 1],
    [1, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 2, 0, 3, 3, 3, 3, 0, 0, 0, 0, 2, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 2, 2, 2, 2, 0, 2, 2, 'X', 2, 2, 0, 2, 0, 2, 0, 2, 0, 1],
    [1, 0, 0, 0, 0, 2, 0, 2, 'X', 'C', 'X', 1, 0, 2, 0, 2, 0, 1, 0, 1],
    [0, 0, 1, 1, 0, 2, 0, 2, 'C', 'C', 'C', 1, 0, 2, 0, 2, 0, 0, 0, 0],
    [1, 0, 1, 1, 0, 2, 0, 2, 1, 1, 1, 1, 0, 2, 0, 2, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 2, 0, 0, 0, 'M', 0, 0, 0, 2, 0, 2, 0, 1, 0, 1],
    [1, 0, 2, 2, 2, 2, 0, 2, 1, 0, 2, 2, 2, 2, 0, 2, 0, 1, 0, 1],
    [1, 0, 2, 'X', 'X', 2, 0, 2, 1, 0, 2, 'X', 'X', 2, 0, 2, 0, 0, 0, 1],
    [1, 0, 2, 'X', 'X', 2, 0, 2, 1, 0, 2, 'X', 'X', 2, 0, 2, 0, 1, 0, 1],
    [1, 0, 2, 2, 2, 2, 0, 2, 1, 0, 2, 2, 2, 2, 0, 2, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]

# Initialize game start time
start_time = time.time()

def draw_grid():
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if grid_layout[y][x] in {1, 2, 3}:
                draw_wall(x * CELL_SIZE, y * CELL_SIZE, get_wall_color(grid_layout[y][x]))
            elif grid_layout[y][x] == 0:
                draw_point(x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2)

def get_wall_color(value):
    if value == 1:
        return WALL_COLOR
    elif value == 2:
        return WALL_COLOR_BRIGHT
    elif value == 3:
        return WALL_COLOR_YELLOW

# Function to draw a wall
def draw_wall(x, y, color):
    glColor3f(*color)
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + CELL_SIZE, y)
    glVertex2f(x + CELL_SIZE, y + CELL_SIZE)
    glVertex2f(x, y + CELL_SIZE)
    glEnd()

# Function to draw a point
def draw_point(x, y):
    glColor3f(*POINT_COLOR)
    glBegin(GL_POLYGON)
    for i in range(20):
        angle = 2 * 3.14159 * i / 20
        glVertex2f(x + 5 * math.cos(angle), y + 5 * math.sin(angle))  # Increase point size
    glEnd()

# Function to draw Momoman
def draw_momoman(x, y):
    glColor3f(*MOMOMAN_COLOR)
    glBegin(GL_POLYGON)
    for i in range(20):
        angle = 2 * 3.14159 * i / 20
        glVertex2f(x + 10 * math.cos(angle), y + 10 * math.sin(angle))  # Increase Momoman size
    glEnd()

# Function to draw a chef
def draw_chef(x, y):
    glColor3f(*CHEF_COLOR)
    glBegin(GL_POLYGON)
    for i in range(20):
        angle = 2 * 3.14159 * i / 20
        glVertex2f(x + 8 * math.cos(angle), y + 8 * math.sin(angle))  # Adjust Chef size
    glEnd()

# Initialize Momoman and chefs
momoman_position = [9, 11]
chefs = [[9, 8], [9, 9], [9, 10]]  # Starting positions of chefs

# Game state variables
direction = [0, 0]
score = 0
game_over = False

# Function to display footer with score
def draw_footer():
    glColor3f(*FOOTER_COLOR)
    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(display[0], 0)
    glVertex2f(display[0], BOTTOM_OFFSET)
    glVertex2f(0, BOTTOM_OFFSET)
    glEnd()

    score_text = f'Score: {score}'
    pygame.font.init()
    font = pygame.font.Font(None, 36)
    text_surface = font.render(score_text, True, (255, 255, 255))
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    glRasterPos2d(10, 10)
    glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)

# Function to handle user input
def handle_input():
    global direction
    keys = pygame.key.get_pressed()
    if keys[K_LEFT]:
        direction = [-1, 0]
    elif keys[K_RIGHT]:
        direction = [1, 0]
    elif keys[K_UP]:
        direction = [0, 1]
    elif keys[K_DOWN]:
        direction = [0, -1]

# Function to move Momoman
def move_momoman():
    global momoman_position, score, game_over
    new_position = [momoman_position[0] + direction[0], momoman_position[1] + direction[1]]
    if can_move_to(new_position):
        momoman_position = new_position
        if grid_layout[momoman_position[1]][momoman_position[0]] == 0:
            score += 10
            grid_layout[momoman_position[1]][momoman_position[0]] = -1  # Mark point as collected

        # Check for teleportation
        if grid_layout[momoman_position[1]][momoman_position[0]] == 'X':
            teleport()
        
        # Check if all points are collected
        if not any(0 in row for row in grid_layout):
            game_over = True

# Function to move chefs
def move_chefs():
    global game_over
    for chef in chefs:
        move_chef(chef)
        if chef == momoman_position:
            game_over = True

# Function to move a single chef
def move_chef(chef):
    move_prob = random.random()
    if move_prob < CHEF_RANDOMNESS_HIGH:
        direction = get_direction_towards_momoman(chef)
    else:
        direction = get_random_direction()
    new_position = [chef[0] + direction[0], chef[1] + direction[1]]
    if can_move_to(new_position):
        chef[0] += direction[0]
        chef[1] += direction[1]

# Function to get a random direction
def get_random_direction():
    return random.choice([[0, 1], [1, 0], [0, -1], [-1, 0]])

# Function to get direction towards Momoman
def get_direction_towards_momoman(chef):
    dx = momoman_position[0] - chef[0]
    dy = momoman_position[1] - chef[1]
    if abs(dx) > abs(dy):
        return [int(math.copysign(1, dx)), 0]
    else:
        return [0, int(math.copysign(1, dy))]

# Function to check if a move is valid
def can_move_to(position):
    x, y = position
    return 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE and grid_layout[y][x] not in {1, 2, 3}

# Function to handle teleportation
def teleport():
    possible_teleport_locations = [(x, y) for y in range(GRID_SIZE) for x in range(GRID_SIZE) if grid_layout[y][x] == 'X' and (x, y) != tuple(momoman_position)]
    if possible_teleport_locations:
        momoman_position[:] = random.choice(possible_teleport_locations)

# Function to display winning screen
def display_winning_screen():
    total_time = time.time() - start_time
    total_score = score

    # Clear screen
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    win_text = f"You Win! Score: {total_score}, Time: {total_time:.2f}s"
    pygame.font.init()
    font = pygame.font.Font(None, 48)
    text_surface = font.render(win_text, True, (255, 255, 255))
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    glRasterPos2d(display[0] // 2 - text_surface.get_width() // 2, display[1] // 2)
    glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)

    pygame.display.flip()

# Main game loop
last_momoman_move = pygame.time.get_ticks()
last_chef_move = pygame.time.get_ticks()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if game_over:
        display_winning_screen()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    handle_input()

    current_time = pygame.time.get_ticks()
    if current_time - last_momoman_move > MOMOMAN_SPEED:
        move_momoman()
        last_momoman_move = current_time

    if current_time - last_chef_move > CHEF_SPEED:
        move_chefs()
        last_chef_move = current_time

    # Clear screen
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(*BACKGROUND_COLOR, 1.0)

    # Draw grid, Momoman, chefs, and footer
    draw_grid()
    draw_momoman(momoman_position[0] * CELL_SIZE + CELL_SIZE // 2, momoman_position[1] * CELL_SIZE + CELL_SIZE // 2)
    for chef in chefs:
        draw_chef(chef[0] * CELL_SIZE + CELL_SIZE // 2, chef[1] * CELL_SIZE + CELL_SIZE // 2)
    draw_footer()

    pygame.display.flip()
    pygame.time.wait(10)
