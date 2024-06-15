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
gluOrtho2D(0, display[0], display[1], 0)  # Flipped vertically

# Constants
GRID_SIZE = 20
CELL_SIZE = display[0] // GRID_SIZE
WALL_WIDTH = 2
BOTTOM_OFFSET = 0

# Colors
MOMOMAN_COLOR = (1, 1, 1)  # White
POINT_COLOR = (1, 0, 0)  # Bright Red
FOOTER_COLOR = (0.2, 0.2, 0.2)  # Dark Gray
WALL_COLOR = (0.7, 0.35, 0)  # Orange
WALL_COLOR_BRIGHT = (1, 0.75, 0)  # Brighter Orange
WALL_COLOR_YELLOW = (0.8, 0.8, 0.8) 
BACKGROUND_COLOR = (0.2, 0.1, 0.1)  # Darker slightly bluish hue
CHEF_COLOR_RED = (1, 0, 0)  # Red
CHEF_COLOR_BLUE = (0, 0, 1)  # Blue
CHEF_COLOR_PINK = (1, 0.5, 1)  # Pink
CHEF_COLOR_GREEN = (0, 1, 0)  # Green

# Speed and randomness settings
MOMOMAN_SPEED = 200  # milliseconds per move
CHEF_SPEED = 250  # milliseconds per move
CHEF_RANDOMNESS_LOW = 0.1  # low randomness for some chefs
CHEF_RANDOMNESS_HIGH = 0.4  # high randomness for other chefs

original_grid_layout = [
   [1, 1, 1, 1, 1, 1, 1, 1, 1, 'A', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
   [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
   [1, 0, 2, 2, 2, 2, 0, 3, 0, 3, 0, 0, 2, 2, 2, 2, 0, 1, 0, 1],
   [1, 0, 2, 'X', 'X', 2, 0, 3, 0, 3, 0, 0, 2, 'X', 'X', 2, 0, 1, 0, 1],
   [1, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 1, 0, 1],
   [1, 0, 0, 0, 0, 2, 0, 3, 3, 3, 3, 0, 0, 0, 0, 2, 0, 0, 0, 1],
   [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
   [1, 0, 2, 2, 2, 2, 0, 2, 2, 'X', 2, 2, 0, 2, 0, 2, 0, 2, 0, 1],
   [1, 0, 0, 0, 0, 2, 0, 2, 'X', 'C', 'X', 1, 0, 2, 0, 2, 0, 1, 0, 1],
   ['Y', 0, 1, 1, 0, 2, 0, 2, 'C', 'C', 'C', 1, 0, 2, 0, 2, 0, 0, 0, 'Z'],
   [1, 0, 1, 1, 0, 2, 0, 2, 1, 1, 1, 1, 0, 2, 0, 2, 0, 1, 0, 1],
   [1, 0, 0, 0, 0, 2, 0, 0, 0, 'M', 0, 0, 0, 2, 0, 2, 0, 1, 0, 1],
   [1, 0, 2, 2, 2, 2, 0, 2, 1, 0, 2, 2, 2, 2, 0, 2, 0, 1, 0, 1],
   [1, 0, 2, 'X', 'X', 2, 0, 2, 1, 0, 2, 'X', 'X', 2, 0, 2, 0, 0, 0, 1],
   [1, 0, 2, 'X', 'X', 2, 0, 2, 1, 0, 2, 'X', 'X', 2, 0, 2, 0, 1, 0, 1],
   [1, 0, 2, 2, 2, 2, 0, 2, 1, 0, 2, 2, 2, 2, 0, 2, 0, 1, 0, 1],
   [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
   [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
   [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
   [1, 1, 1, 1, 1, 1, 1, 1, 1, 'B', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

grid_layout = [row[:] for row in original_grid_layout]
grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]

def reset_grid():
   global grid_layout
   grid_layout = [row[:] for row in original_grid_layout]

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
def draw_wall(x, y, color):
  glColor3f(*color)
  glBegin(GL_QUADS)
  glVertex2f(x, y)
  glVertex2f(x + CELL_SIZE, y)
  glVertex2f(x + CELL_SIZE, y + CELL_SIZE)
  glVertex2f(x, y + CELL_SIZE)
  glEnd()

def draw_point(x, y):
  glColor3f(*POINT_COLOR)
  glBegin(GL_POLYGON)
  for i in range(20):
      angle = 2 * 3.14159 * i / 20
      glVertex2f(x + 5 * math.cos(angle), y + 5 * math.sin(angle))
  glEnd()

def draw_momoman(x, y, mouth_open, direction):
  glColor3f(*MOMOMAN_COLOR)
  glBegin(GL_POLYGON)
  for i in range(20):
      angle = 2 * 3.14159 * i / 20
      glVertex2f(x + 15 * math.cos(angle), y + 15 * math.sin(angle))
  glEnd()

  if mouth_open == 1:
      glColor3f(*BACKGROUND_COLOR)
      glBegin(GL_POLYGON)
      if direction == 'UP' or direction == 'DOWN':
          if direction == 'UP':
              glVertex2f(x, y)
              glVertex2f(x - 15, y - 15)
              glVertex2f(x + 15, y - 15)
          else:
              glVertex2f(x, y)
              glVertex2f(x - 15, y + 15)
              glVertex2f(x + 15, y + 15)
      elif direction == 'LEFT' or direction == 'RIGHT':
          if direction == 'LEFT':
              glVertex2f(x, y)
              glVertex2f(x - 15, y - 15)
              glVertex2f(x - 15, y + 15)
          else:
              glVertex2f(x, y)
              glVertex2f(x + 15, y - 15)
              glVertex2f(x + 15, y + 15)
      glEnd()
  elif mouth_open == 2:
      glColor3f(*WALL_COLOR)
      glBegin(GL_POLYGON)
      glVertex2f(x, y)
      glVertex2f(x - 15, y - 15)
      glVertex2f(x - 15, y + 15)
      glEnd()

def draw_chef(x, y, color, direction):
  

  # Draw cap to indicate direction
  glColor3f(*MOMOMAN_COLOR)
  if direction == 'UP':
      glBegin(GL_QUADS)
      glVertex2f(x - 10, y)
      glVertex2f(x + 10, y)
      glVertex2f(x + 12, y + 30)
      glVertex2f(x - 12, y + 30)
      glColor3f(*color)
      glVertex2f(x-1,y)
      glVertex2f(x-2,y + 25)
      glVertex2f(x+2,y+25)
      glVertex2f(x+1,y)
      glEnd()
  elif direction == 'DOWN':
      glBegin(GL_QUADS)
      glVertex2f(x - 12, y - 30)
      glVertex2f(x + 12, y - 30)
      glVertex2f(x + 10, y)
      glVertex2f(x - 10, y)
      glColor3f(*color)
      glVertex2f(x-2,y - 25)
      glVertex2f(x-1,y)
      glVertex2f(x+1,y)
      glVertex2f(x+2,y - 25)
      glEnd()
  elif direction == 'LEFT':
      glBegin(GL_QUADS)
      glVertex2f(x - 30, y - 10)
      glVertex2f(x, y - 8)
      glVertex2f(x, y + 8)
      glVertex2f(x - 30, y + 10)
      glColor3f(*color)
      glVertex2f(x - 25,y+1)
      glVertex2f(x - 25,y+2)
      glVertex2f(x,y+2)
      glVertex2f(x,y+1)
      glEnd()
  else:  # 'RIGHT'
      glBegin(GL_QUADS)
      glVertex2f(x, y - 8)
      glVertex2f(x + 30, y - 10)
      glVertex2f(x + 30, y + 10)
      glVertex2f(x, y + 8)
      glColor3f(*color)
      glVertex2f(x+25,y + 1)
      glVertex2f(x+25,y + 2)
      glVertex2f(x,y + 2)
      glVertex2f(x,y + 1)
      glEnd()

  glColor3f(*color)
  glBegin(GL_POLYGON)
  for i in range(80):
      angle = 2 * 3.14159 * i / 20
      glVertex2f(x + 15 * math.cos(angle), y + 10 * math.sin(angle))  # Make chef shape slightly elliptical
  glEnd()

def draw_footer(score, lives):
  glColor3f(*FOOTER_COLOR)
  glBegin(GL_QUADS)
  glVertex2f(0, display[1])
  glVertex2f(display[0], display[1])
  glVertex2f(display[0], display[1] - BOTTOM_OFFSET)
  glVertex2f(0, display[1] - BOTTOM_OFFSET)
  glEnd()

  glColor3f(1, 1, 1)
  glRasterPos2f(10, display[1] - 20)
  for char in f"Score: {score}":
      glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

  for i in range(lives):
      draw_momoman(display[0] - 30 - i * 40, display[1] - 20, 2, 'LEFT')

def grid_to_screen(x, y):
  return x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2

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
              f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
              heapq.heappush(open_set, (f_score[neighbor], neighbor))

  return []

def heuristic(a, b):
  return abs(a[0] - b[0]) + abs(a[1] - b[1])

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

momoman_pos = (9, 11)
chef_positions = [(10, 9), (8, 9), (10, 8), (8, 8)]
chef_colors = [CHEF_COLOR_RED, CHEF_COLOR_BLUE,CHEF_COLOR_PINK, CHEF_COLOR_GREEN]
chef_directions = ['RIGHT', 'RIGHT', 'LEFT', 'LEFT']  # Initial directions for chefs
points = 0
lives = 4
momoman_mouth_open = True
momoman_direction = 'RIGHT'
momoman_target_pos = momoman_pos

def reset_game():
  global momoman_pos, chef_positions, points, lives, momoman_mouth_open, momoman_direction, momoman_target_pos
  reset_grid()
  momoman_pos = (9, 11)
  chef_positions = [(10, 9), (8, 9), (10, 8), (8, 8)]
  chef_directions = ['RIGHT', 'RIGHT', 'LEFT', 'LEFT']  # Reset chef directions
  points = 0
  lives = 4
  momoman_mouth_open = True
  momoman_direction = 'RIGHT'
  momoman_target_pos = momoman_pos

def start_screen():
  glClear(GL_COLOR_BUFFER_BIT)
  glColor3f(*WALL_COLOR_YELLOW)
  text = "MomoMan"
  
  text_width = len(text) * 18
  x_position = (display[0] - text_width) / 2
  glRasterPos2f(x_position, display[1] // 2)
  for char in text:
      glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(char))

  enter_text = "Press Enter to start game"
  enter_text_width = len(enter_text) * 9
  x_position = (display[0] - enter_text_width) / 2
  glRasterPos2f(x_position, display[1] // 2 + 60)
  for char in enter_text:
      glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

  pygame.display.flip()
  while True:
      for event in pygame.event.get():
          if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
              return
          elif event.type == pygame.QUIT:
              pygame.quit()
              sys.exit()

def start_game():
  global momoman_pos, chef_positions, points, lives, momoman_mouth_open, momoman_direction, momoman_target_pos

  reset_game()

  momoman_last_move_time = 0
  chef_last_move_time = 0
#   chef_blue_direction = 'RIGHT'
#   chef_blue_pos = (1, 1)
  running = True
  while running:
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
                  momoman_target_pos = (momoman_pos[0], momoman_pos[1] - 1)
              elif event.key == pygame.K_DOWN:
                  momoman_direction = 'DOWN'
                  momoman_target_pos = (momoman_pos[0], momoman_pos[1] + 1)
              elif event.key == pygame.K_LEFT:
                  momoman_direction = 'LEFT'
                  momoman_target_pos = (momoman_pos[0] - 1, momoman_pos[1])
              elif event.key == pygame.K_RIGHT:
                  momoman_direction = 'RIGHT'
                  momoman_target_pos = (momoman_pos[0] + 1, momoman_pos[1])

      current_time = pygame.time.get_ticks()
      if current_time - momoman_last_move_time > MOMOMAN_SPEED:
          x, y = momoman_pos
          new_pos = momoman_pos

          if momoman_direction == 'UP' and y > 0 and grid_layout[y - 1][x] not in {1, 2, 3}:
              new_pos = (x, y - 1)
          elif momoman_direction == 'DOWN' and y < GRID_SIZE - 1 and grid_layout[y + 1][x] not in {1, 2, 3}:
              new_pos = (x, y + 1)
          elif momoman_direction == 'LEFT' and x > 0 and grid_layout[y][x - 1] not in {1, 2, 3}:
              new_pos = (x - 1, y)
          elif momoman_direction == 'RIGHT' and x < GRID_SIZE - 1 and grid_layout[y][x + 1] not in {1, 2, 3}:
              new_pos = (x + 1, y)

          if new_pos != momoman_pos:
              momoman_pos = new_pos
              if grid_layout[momoman_pos[1]][momoman_pos[0]] == 0:
                  points += 1
                  grid_layout[momoman_pos[1]][momoman_pos[0]] = -1

              # Teleportation
              if grid_layout[momoman_pos[1]][momoman_pos[0]] == 'A':
                  momoman_pos = next((j, i) for i, row in enumerate(grid_layout) for j, cell in enumerate(row) if cell == 'B')
              elif grid_layout[momoman_pos[1]][momoman_pos[0]] == 'B':
                  momoman_pos = next((j, i) for i, row in enumerate(grid_layout) for j, cell in enumerate(row) if cell == 'A')
              elif grid_layout[momoman_pos[1]][momoman_pos[0]] == 'Y':
                  momoman_pos = next((j, i) for i, row in enumerate(grid_layout) for j, cell in enumerate(row) if cell == 'Z')
              elif grid_layout[momoman_pos[1]][momoman_pos[0]] == 'Z':
                  momoman_pos = next((j, i) for i, row in enumerate(grid_layout) for j, cell in enumerate(row) if cell == 'Y')

          momoman_mouth_open = not momoman_mouth_open
          momoman_last_move_time = current_time

      if current_time - chef_last_move_time > CHEF_SPEED:
          for i in range(4):
              chef_pos = chef_positions[i]
              if i == 0:  # Red chef follows MomoMan with lowest randomness
                  randomness = CHEF_RANDOMNESS_LOW
                  if random.random() < randomness:
                      chef_positions[i] = random.choice(get_neighbors(chef_pos))
                      chef_directions[i] = get_direction_from_position(chef_positions[i], chef_pos)
                  else:
                      path = astar(chef_pos, momoman_pos)
                      if path:
                          chef_positions[i] = path[0]
                          chef_directions[i] = get_direction_from_position(chef_positions[i], chef_pos)
              elif i == 1:  # Blue chef follows a pattern
                  randomness = CHEF_RANDOMNESS_HIGH
                  if random.random() < randomness:
                      chef_positions[i] = random.choice(get_neighbors(chef_pos))
                      chef_directions[i] = get_direction_from_position(chef_positions[i], chef_pos)
                  else:
                      path = astar(chef_pos, momoman_pos)
                      if path:
                          chef_positions[i] = path[0]
                          chef_directions[i] = get_direction_from_position(chef_positions[i], chef_pos)
                #   if chef_blue_pos[1] == 2 and chef_blue_pos[0] < GRID_SIZE - 1 and grid_layout[chef_blue_pos[1]][chef_blue_pos[0] + 1] not in {1, 2, 3}:
                #       chef_blue_pos = (chef_blue_pos[0] + 1, chef_blue_pos[1])
                #       chef_blue_direction = 'RIGHT'
                #   elif chef_blue_pos[0] == GRID_SIZE - 1 and chef_blue_pos[1] < GRID_SIZE - 1 and grid_layout[chef_blue_pos[1] + 1][chef_blue_pos[0]] not in {1, 2, 3}:
                #       chef_blue_pos = (chef_blue_pos[0], chef_blue_pos[1] + 1)
                #       chef_blue_direction = 'DOWN'
                #   elif chef_blue_pos[1] == GRID_SIZE - 1 and chef_blue_pos[0] > 0 and grid_layout[chef_blue_pos[1]][chef_blue_pos[0] - 1] not in {1, 2, 3}:
                #       chef_blue_pos = (chef_blue_pos[0] - 1, chef_blue_pos[1])
                #       chef_blue_direction = 'LEFT'
                #   elif chef_blue_pos[0] == 0 and chef_blue_pos[1] > 2 and grid_layout[chef_blue_pos[1] - 1][chef_blue_pos[0]] not in {1, 2, 3}:
                #       chef_blue_pos = (chef_blue_pos[0], chef_blue_pos[1] - 1)
                #       chef_blue_direction = 'UP'
                #   chef_positions[i] = chef_blue_pos
                #   chef_directions[i] = chef_blue_direction
              elif i == 2:  # Pink chef moves randomly
                  randomness = CHEF_RANDOMNESS_HIGH
                  chef_positions[i] = random.choice(get_neighbors(chef_pos))
                  chef_directions[i] = get_direction_from_position(chef_positions[i], chef_pos)
              else:  # Green chef follows MomoMan with lowest randomness
                  randomness = CHEF_RANDOMNESS_LOW
                  if random.random() < randomness:
                      chef_positions[i] = random.choice(get_neighbors(chef_pos))
                      chef_directions[i] = get_direction_from_position(chef_positions[i], chef_pos)
                  else:
                      path = astar(chef_pos, momoman_pos)
                      if path:
                          chef_positions[i] = path[0]
                          chef_directions[i] = get_direction_from_position(chef_positions[i], chef_pos)

          chef_last_move_time = current_time

      for i, chef_pos in enumerate(chef_positions):
          if momoman_pos == chef_pos:
              lives -= 1
              if lives == 0:
                  running = False
                  game_over_screen()
              else:
                  momoman_pos = (9, 11)

      glClear(GL_COLOR_BUFFER_BIT)
      draw_grid()
      draw_momoman(*grid_to_screen(*momoman_pos), momoman_mouth_open, momoman_direction)
      for i, chef_pos in enumerate(chef_positions):
          draw_chef(*grid_to_screen(*chef_pos), chef_colors[i], chef_directions[i])
      draw_footer(points, lives)
      pygame.display.flip()
      pygame.time.wait(10)

      # New code for the blue chef to move in circles
    #   if chef_blue_pos == (1, 1):
    #       chef_blue_direction = 'RIGHT'
    #   elif chef_blue_pos == (GRID_SIZE - 1, 1):
    #       chef_blue_direction = 'DOWN'
    #   elif chef_blue_pos == (GRID_SIZE - 1, GRID_SIZE - 1):
    #       chef_blue_direction = 'LEFT'
    #   elif chef_blue_pos == (1, GRID_SIZE - 1):
    #       chef_blue_direction = 'UP'

    #   if chef_blue_direction == 'UP':
    #       new_chef_blue_pos = (chef_blue_pos[0], chef_blue_pos[1] - 1)
    #   elif chef_blue_direction == 'DOWN':
    #       new_chef_blue_pos = (chef_blue_pos[0], chef_blue_pos[1] + 1)
    #   elif chef_blue_direction == 'LEFT':
    #       new_chef_blue_pos = (chef_blue_pos[0] - 1, chef_blue_pos[1])
    #   else:
    #       new_chef_blue_pos = (chef_blue_pos[0] + 1, chef_blue_pos[1])

    #   if grid_layout[new_chef_blue_pos[1]][new_chef_blue_pos[0]] not in {1, 2, 3}:
    #       chef_blue_pos = new_chef_blue_pos
    #       chef_positions[1] = chef_blue_pos
    #       chef_directions[1] = chef_blue_direction

def get_direction_from_position(new_pos, old_pos):
  if new_pos[0] < old_pos[0]:
      return 'LEFT'
  elif new_pos[0] > old_pos[0]:
      return 'RIGHT'
  elif new_pos[1] < old_pos[1]:
      return 'UP'
  else:
      return 'DOWN'

def game_over_screen():
  global points
  glClear(GL_COLOR_BUFFER_BIT)
  glColor3f(1, 1, 1)

  text = "Game Over!"
  text_width = len(text) * 9
  x_position = (display[0] - text_width) / 2
  glRasterPos2f(x_position, display[1] // 2)
  for char in text:
      glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

  score_text = "Score: " + str(points)
  score_text_width = len(score_text) * 9
  x_position = (display[0] - score_text_width) / 2
  glRasterPos2f(x_position, display[1] // 2 + 30)
  for char in score_text:
      glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

  enter_text = "Press Enter to play again"
  enter_text_width = len(enter_text) * 9
  x_position = (display[0] - enter_text_width) / 2
  glRasterPos2f(x_position, display[1] // 2 + 60)
  for char in enter_text:
      glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

  pygame.display.flip()
  while True:
      for event in pygame.event.get():
          if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
              reset_game()
              start_game()
          elif event.type == pygame.QUIT:
              pygame.quit()
              sys.exit()

# New code for the "Congratulations!" screen
def congratulations_screen():
  glClear(GL_COLOR_BUFFER_BIT)
  glColor3f(1, 1, 1)

  text = "Congratulations!!!"
  text_width = len(text) * 18
  x_position = (display[0] - text_width) / 2
  glRasterPos2f(x_position, display[1] // 2)
  for char in text:
      glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(char))

  text = "You have completed the game!"
  text_width = len(text) * 9
  x_position = (display[0] - text_width) / 2
  glRasterPos2f(x_position, display[1] // 2 + 30)
  for char in text:
      glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

  enter_text = "Press Enter to play again"
  enter_text_width = len(enter_text) * 9
  x_position = (display[0] - enter_text_width) / 2
  glRasterPos2f(x_position, display[1] // 2 + 60)
  for char in enter_text:
      glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

  pygame.display.flip()
  while True:
      for event in pygame.event.get():
          if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
              reset_game()
              start_game()
          elif event.type == pygame.QUIT:
              pygame.quit()
              sys.exit()

# Start the game
start_screen()
start_game()

# Check for the "Congratulations!" condition
def check_congratulations():
  for row in grid_layout:
      if 0 in row:
          return False
  congratulations_screen()
  return True

# Call check_congratulations() after momoman_pos is updated
def start_game():
   global momoman_pos, chef_positions, points, lives, momoman_mouth_open, momoman_direction, momoman_target_pos

   reset_game()

   momoman_last_move_time = 0
   chef_last_move_time = 0
   chef_blue_direction = 'RIGHT'
   chef_blue_pos = (1, 1)
   running = True
   while running:
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
                   momoman_target_pos = (momoman_pos[0], momoman_pos[1] - 1)
               elif event.key == pygame.K_DOWN:
                   momoman_direction = 'DOWN'
                   momoman_target_pos = (momoman_pos[0], momoman_pos[1] + 1)
               elif event.key == pygame.K_LEFT:
                   momoman_direction = 'LEFT'
                   momoman_target_pos = (momoman_pos[0] - 1, momoman_pos[1])
               elif event.key == pygame.K_RIGHT:
                   momoman_direction = 'RIGHT'
                   momoman_target_pos = (momoman_pos[0] + 1, momoman_pos[1])

       current_time = pygame.time.get_ticks()
       if current_time - momoman_last_move_time > MOMOMAN_SPEED:
           x, y = momoman_pos
           new_pos = momoman_pos

           if momoman_direction == 'UP' and y > 0 and grid_layout[y - 1][x] not in {1, 2, 3}:
               new_pos = (x, y - 1)
           elif momoman_direction == 'DOWN' and y < GRID_SIZE - 1 and grid_layout[y + 1][x] not in {1, 2, 3}:
               new_pos = (x, y + 1)
           elif momoman_direction == 'LEFT' and x > 0 and grid_layout[y][x - 1] not in {1, 2, 3}:
               new_pos = (x - 1, y)
           elif momoman_direction == 'RIGHT' and x < GRID_SIZE - 1 and grid_layout[y][x + 1] not in {1, 2, 3}:
               new_pos = (x + 1, y)

           if new_pos != momoman_pos:
               momoman_pos = new_pos
               if grid_layout[momoman_pos[1]][momoman_pos[0]] == 0:
                   points += 1
                   grid_layout[momoman_pos[1]][momoman_pos[0]] = -1

               # Teleportation
               if grid_layout[momoman_pos[1]][momoman_pos[0]] == 'A':
                   momoman_pos = next((j, i) for i, row in enumerate(grid_layout) for j, cell in enumerate(row) if cell == 'B')
               elif grid_layout[momoman_pos[1]][momoman_pos[0]] == 'B':
                   momoman_pos = next((j, i) for i, row in enumerate(grid_layout) for j, cell in enumerate(row) if cell == 'A')
               elif grid_layout[momoman_pos[1]][momoman_pos[0]] == 'Y':
                   momoman_pos = next((j, i) for i, row in enumerate(grid_layout) for j, cell in enumerate(row) if cell == 'Z')
               elif grid_layout[momoman_pos[1]][momoman_pos[0]] == 'Z':
                   momoman_pos = next((j, i) for i, row in enumerate(grid_layout) for j, cell in enumerate(row) if cell == 'Y')

           momoman_mouth_open = not momoman_mouth_open
           momoman_last_move_time = current_time

       if current_time - chef_last_move_time > CHEF_SPEED:
           for i in range(4):
               chef_pos = chef_positions[i]
               if i == 0:  # Red chef follows MomoMan with lowest randomness
                   randomness = CHEF_RANDOMNESS_LOW
                   if random.random() < randomness:
                       chef_positions[i] = random.choice(get_neighbors(chef_pos))
                       chef_directions[i] = get_direction_from_position(chef_positions[i], chef_pos)
                   else:
                       path = astar(chef_pos, momoman_pos)
                       if path:
                           chef_positions[i] = path[0]
                           chef_directions[i] = get_direction_from_position(chef_positions[i], chef_pos)
               elif i == 1:  # Blue chef follows a pattern
                   randomness = CHEF_RANDOMNESS_LOW
                   if random.random() < randomness:
                       chef_positions[i] = random.choice(get_neighbors(chef_pos))
                       chef_directions[i] = get_direction_from_position(chef_positions[i], chef_pos)
                   else:
                       path = astar(chef_pos, momoman_pos)
                       if path:
                           chef_positions[i] = path[0]
                           chef_directions[i] = get_direction_from_position(chef_positions[i], chef_pos)
               elif i == 2:  # Pink chef moves randomly
                   randomness = CHEF_RANDOMNESS_HIGH
                   chef_positions[i] = random.choice(get_neighbors(chef_pos))
                   chef_directions[i] = get_direction_from_position(chef_positions[i], chef_pos)
               else:  # Green chef follows MomoMan with lowest randomness
                   randomness = CHEF_RANDOMNESS_LOW
                   if random.random() < randomness:
                       chef_positions[i] = random.choice(get_neighbors(chef_pos))
                       chef_directions[i] = get_direction_from_position(chef_positions[i], chef_pos)
                   else:
                       path = astar(chef_pos, momoman_pos)
                       if path:
                           chef_positions[i] = path[0]
                           chef_directions[i] = get_direction_from_position(chef_positions[i], chef_pos)

           chef_last_move_time = current_time

       for i, chef_pos in enumerate(chef_positions):
           if momoman_pos == chef_pos:
               lives -= 1
               if lives == 0:
                   running = False
                   game_over_screen()
               else:
                   momoman_pos = (9, 11)

       glClear(GL_COLOR_BUFFER_BIT)
       draw_grid()
       draw_momoman(*grid_to_screen(*momoman_pos), momoman_mouth_open, momoman_direction)
       for i, chef_pos in enumerate(chef_positions):
           draw_chef(*grid_to_screen(*chef_pos), chef_colors[i], chef_directions[i])
       draw_footer(points, lives)
       pygame.display.flip()
       pygame.time.wait(10)

    #    # New code for the blue chef to move in circles
    #    if chef_blue_pos == (1, 1):
    #        chef_blue_direction = 'RIGHT'
    #    elif chef_blue_pos == (GRID_SIZE - 1, 1):
    #        chef_blue_direction = 'DOWN'
    #    elif chef_blue_pos == (GRID_SIZE - 1, GRID_SIZE - 1):
    #        chef_blue_direction = 'LEFT'
    #    elif chef_blue_pos == (1, GRID_SIZE - 1):
    #        chef_blue_direction = 'UP'

    #    if chef_blue_direction == 'UP':
    #        new_chef_blue_pos = (chef_blue_pos[0], chef_blue_pos[1] - 1)
    #    elif chef_blue_direction == 'DOWN':
    #        new_chef_blue_pos = (chef_blue_pos[0], chef_blue_pos[1] + 1)
    #    elif chef_blue_direction == 'LEFT':
    #        new_chef_blue_pos = (chef_blue_pos[0] - 1, chef_blue_pos[1])
    #    else:
    #        new_chef_blue_pos = (chef_blue_pos[0] + 1, chef_blue_pos[1])

    #    if grid_layout[new_chef_blue_pos[1]][new_chef_blue_pos[0]] not in {1, 2, 3}:
    #        chef_blue_pos = new_chef_blue_pos
    #        chef_positions[1] = chef_blue_pos
    #        chef_directions[1] = chef_blue_direction

       if check_congratulations():
           running = False

start_screen()
start_game()
