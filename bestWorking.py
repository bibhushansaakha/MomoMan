import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import random
import heapq
import math


# Initialize pygame and OpenGL
pygame.init()
display = (800, 800)  # Display size
pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)
gluOrtho2D(0, display[0], 0, display[1])

# Constants
GRID_SIZE = 20  # Adjusted grid size to fit new window size
# Adjust cell size dynamically based on grid size and display width
CELL_SIZE = display[0] // GRID_SIZE
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
MOMOMAN_SPEED = 200  # milliseconds per move
CHEF_SPEED = 500  # milliseconds per move
CHEF_RANDOMNESS_LOW = 0.2  # low randomness for some chefs
CHEF_RANDOMNESS_HIGH = 0.8  # high randomness for other chefs

global grid_layout

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


def reset_grid():
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


def draw_grid():
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if grid_layout[y][x] in {1, 2, 3}:
                draw_wall(x * CELL_SIZE, y * CELL_SIZE,
                          get_wall_color(grid_layout[y][x]))
            elif grid_layout[y][x] == 0:
                draw_point(x * CELL_SIZE + CELL_SIZE // 2,
                           y * CELL_SIZE + CELL_SIZE // 2)


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
        glVertex2f(x + 5 * math.cos(angle), y + 5 *
                   math.sin(angle))  # Increase point size
    glEnd()

# Function to draw MomoMan


def draw_momoman(x, y, mouth_open, direction):
    glColor3f(*MOMOMAN_COLOR)
    glBegin(GL_POLYGON)
    for i in range(20):
        angle = 2 * 3.14159 * i / 20
        glVertex2f(x + 15 * math.cos(angle), y + 15 *
                   math.sin(angle))  # Increase MomoMan size
    glEnd()

    if mouth_open:
        glColor3f(*BACKGROUND_COLOR)
        glBegin(GL_POLYGON)
        if direction == 'UP':
            glVertex2f(x, y)
            glVertex2f(x - 15, y + 15)
            glVertex2f(x + 15, y + 15)
        elif direction == 'DOWN':
            glVertex2f(x, y)
            glVertex2f(x - 15, y - 15)
            glVertex2f(x + 15, y - 15)
        elif direction == 'LEFT':
            glVertex2f(x, y)
            glVertex2f(x - 15, y - 15)
            glVertex2f(x - 15, y + 15)
        elif direction == 'RIGHT':
            glVertex2f(x, y)
            glVertex2f(x + 15, y - 15)
            glVertex2f(x + 15, y + 15)
        glEnd()

# Function to draw a chef


def draw_chef(x, y):
    glColor3f(*CHEF_COLOR)
    glBegin(GL_POLYGON)
    for i in range(20):
        angle = 2 * 3.14159 * i / 20
        glVertex2f(x + 15 * math.cos(angle), y + 15 *
                   math.sin(angle))  # Increase Chef size
    glEnd()

# Function to draw footer


def draw_footer(score, lives):
    glColor3f(*FOOTER_COLOR)
    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(display[0], 0)
    glVertex2f(display[0], BOTTOM_OFFSET)
    glVertex2f(0, BOTTOM_OFFSET)
    glEnd()

    # Draw the score
    glColor3f(1, 1, 1)
    glRasterPos2f(10, 10)
    for char in f"Score: {score}":
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

    # Draw the lives
    glRasterPos2f(display[0] - 150, 10)
    for char in f"Lives: {lives}":
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

# Utility function to convert grid coordinates to screen coordinates


def grid_to_screen(x, y):
    return x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2

# A* pathfinding algorithm


def astar(start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        for neighbor in get_neighbors(current):
            tentative_g_score = g_score[current] + 1

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + \
                    heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return []

# Heuristic function for A*


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Get neighbors for A*


def get_neighbors(pos):
    x, y = pos
    neighbors = []
    if x > 0 and grid_layout[y][x - 1] not in {1, 2, 3}:
        neighbors.append((x - 1, y))
    if x < GRID_SIZE - 1 and grid_layout[y][x + 1] not in {1, 2, 3}:
        neighbors.append((x + 1, y))
    if y > 0 and grid_layout[y - 1][x] not in {1, 2, 3}:
        neighbors.append((x, y - 1))
    if y < GRID_SIZE - 1 and grid_layout[y + 1][x] not in {1, 2, 3}:
        neighbors.append((x, y + 1))
    return neighbors


# Game state variables
momoman_pos = (9, 11)
# Initial positions for four chefs
chef_positions = [(10, 9), (8, 9), (10, 8), (8, 8)]
points = 0
lives = 3
momoman_mouth_open = True
momoman_direction = 'RIGHT'
momoman_target_pos = momoman_pos

# Main game loop
momoman_last_move_time = 0
chef_last_move_time = 0
running = True


def start_game():
    # Game state variables
    momoman_pos = (9, 11)
    # Initial positions for four chefs
    chef_positions = [(10, 9), (8, 9), (10, 8), (8, 8)]
    points = 0
    lives = 3
    momoman_mouth_open = True
    momoman_direction = 'RIGHT'
    momoman_target_pos = momoman_pos
    reset_grid()
    # Main game loop
    momoman_last_move_time = 0
    chef_last_move_time = 0
    running = True
    while running:
        if points == 181:
            running = False
            game_over_screen(points=points)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_UP:
                    momoman_direction = 'UP'
                    momoman_target_pos = (momoman_pos[0], momoman_pos[1] + 1)
                elif event.key == pygame.K_DOWN:
                    momoman_direction = 'DOWN'
                    momoman_target_pos = (momoman_pos[0], momoman_pos[1] - 1)
                elif event.key == pygame.K_LEFT:
                    momoman_direction = 'LEFT'
                    momoman_target_pos = (momoman_pos[0] - 1, momoman_pos[1])
                elif event.key == pygame.K_RIGHT:
                    momoman_direction = 'RIGHT'
                    momoman_target_pos = (momoman_pos[0] + 1, momoman_pos[1])

        # Move MomoMan
        current_time = pygame.time.get_ticks()
        if current_time - momoman_last_move_time > MOMOMAN_SPEED:
            x, y = momoman_pos
            new_pos = momoman_pos

            if momoman_direction == 'UP' and y < GRID_SIZE - 1 and grid_layout[y + 1][x] not in {1, 2, 3}:
                new_pos = (x, y + 1)
            elif momoman_direction == 'DOWN' and y > 0 and grid_layout[y - 1][x] not in {1, 2, 3}:
                new_pos = (x, y - 1)
            elif momoman_direction == 'LEFT' and x > 0 and grid_layout[y][x - 1] not in {1, 2, 3}:
                new_pos = (x - 1, y)
            elif momoman_direction == 'RIGHT' and x < GRID_SIZE - 1 and grid_layout[y][x + 1] not in {1, 2, 3}:
                new_pos = (x + 1, y)

            if new_pos != momoman_pos:
                momoman_pos = new_pos
                # Eat the point if present
                if grid_layout[y][x] == 0:
                    points += 1
                    grid_layout[y][x] = -1  # Mark the point as eaten

            momoman_mouth_open = not momoman_mouth_open
            momoman_last_move_time = current_time

        # Move Chefs
        if current_time - chef_last_move_time > CHEF_SPEED:
            for i in range(4):
                chef_pos = chef_positions[i]
                if i < 2:  # Less randomness
                    randomness = CHEF_RANDOMNESS_LOW
                else:  # More randomness
                    randomness = CHEF_RANDOMNESS_HIGH

                if random.random() < randomness:
                    chef_positions[i] = random.choice(get_neighbors(chef_pos))
                else:
                    path = astar(chef_pos, momoman_pos)
                    if path:
                        chef_positions[i] = path[0]

            chef_last_move_time = current_time

        # Check collision with Chef
        for chef_pos in chef_positions:
            if momoman_pos == chef_pos:
                lives -= 1
                if lives == 0:
                    running = False  # End the game if MomoMan collides with a Chef
                    game_over_screen(points=points)
                else:
                    momoman_pos = (9, 11)  # Reset MomoMan position

        # Render everything
        glClear(GL_COLOR_BUFFER_BIT)
        draw_grid()
        draw_momoman(*grid_to_screen(*momoman_pos),
                     momoman_mouth_open, momoman_direction)
        for chef_pos in chef_positions:
            draw_chef(*grid_to_screen(*chef_pos))
        draw_footer(points, lives)
        pygame.display.flip()
        pygame.time.wait(10)


def game_over_screen(screen_width=800, screen_height=800, points=points):
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1, 1, 1)

    # Center "Game Over!"
    if points == 181:
        text = "You Win!"
    else:
        text = "Game Over!"
    text_width = len(text) * 9  # Approx width of each character in pixels
    x_position = (screen_width - text_width) / 2
    glRasterPos2f(x_position, 400)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

    # Center "Score: "
    score_text = "Score: " + str(points)
    # Approx width of each character in pixels
    score_text_width = len(score_text) * 9
    x_position = (screen_width - score_text_width) / 2
    glRasterPos2f(x_position, 300)
    for char in score_text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

    # Center "Press Enter to play again"
    enter_text = "Press Enter to play again"
    # Approx width of each character in pixels
    enter_text_width = len(enter_text) * 9
    x_position = (screen_width - enter_text_width) / 2
    glRasterPos2f(x_position, 200)
    for char in enter_text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                lives = 3
                reset_grid()
                start_game()
            elif event.type == pygame.QUIT:
                return False


# start gameloop
start_game()
