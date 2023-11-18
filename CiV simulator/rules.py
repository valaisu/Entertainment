import pygame
import sys
import math
import numpy as np


"""
The goal is to create rules to play a bit of Civilization
More specifically, this program aims to be a small-scale 
battle simulator for 2+ units.

Roadmap:
Create the board from hexagons CHECK
    draw the hexagons CHECK
    add hills, rivers, forests
Create the units 
    unit movement
    unit attack
    turns

side task: improve graphics
    nice pictures
    animations

"""


# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 50  # Size of each hexagon tile

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# positive directions are y: up, x, up-right
# but as the hexagon has 6 sides, some re-defining needs to be made
directions = [(0, 1), (1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1)]


class square:
    def __init__(self, x, y, size, terrain):
        self.x = x
        self.y = y
        self.size = size
        self.terrain = terrain


def are_neighbors(s1, s2):
    """
    Checks, weather squares are adjacent to each other
    :param s1: square
    :param s2: square
    :return: Bool
    """
    return (s1.x-s2.x, s1.y-s2.y) in directions


def create_board(amount: int, size: float):
    """
    Creates a hexagon shaped board, whose diameter is 1+2*amount hexes
    :param amount:
    :param size:
    :return: list[square]
    """
    hexes = [square(0,0,50, 0)]
    tot = 0
    for i in range(amount):
        for dir in range(len(directions)):
            for j in range(i+1):
                tot += 1
                x = (i+1)*directions[dir][0] + j*directions[(dir-2)%6][0]
                y = (i+1)*directions[dir][1] + j*directions[(dir-2)%6][1]
                hexes.append(square(x, y, size, 0))
    return hexes


# Function to draw a hexagon
def draw_hexagon(surface, x: int, y: int, size: float, center: (int, int)):
    """
    Draws a single hexagon using information from the square-class and
    information about the surface
    :param surface:
    :param x: int
    :param y: int
    :param size: float
    :param center: (int, int)
    :return: None
    """
    base_location = (np.cos(np.pi/6)*2*x*size*np.sin(np.pi/3), np.cos(np.pi/6)*(y + x*np.cos(np.pi/3))*2*size)
    angle = np.pi/3
    points = []
    for i in range(6):
        x_i = x + size * math.cos(angle * i) + base_location[0] + center[0]
        y_i = y + size * math.sin(angle * i) + base_location[1] + center[1]
        points.append((x_i, y_i))
    pygame.draw.polygon(surface, WHITE, points, 2)


# Function to draw the hexagon board
def draw_hexagon_board(surface, squares: list[square]):
    """
    Loops through the hexagons and individually draws them
    :param surface:
    :param squares: list[square]
    :return: None
    """
    for sq in squares:
        draw_hexagon(surface, sq.x, sq.y, sq.size, (400, 300))


hexagons = create_board(2, 50)
# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Hexagon Board')

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(BLACK)

    # Draw the hexagon board (5x5 in this example)
    draw_hexagon_board(screen, hexagons)

    pygame.display.flip()




