import copy

import pygame
import sys
import math
import numpy as np
import random


"""
The goal is to create rules to play a bit of Civilization
More specifically, this program aims to be a small-scale 
battle simulator for 2+ units.

Roadmap:
Create the board from hexagons CHECK
    draw the hexagons CHECK
    add hills, rivers, forests CHECK
Create the units 
    unit movement CHECK
    display unit stats
    unit attack
    turns

side task: improve graphics
    nice pictures
    animations

"""


class Button:
    def __init__(self, x, y, image, image_selected, select_radius, offset):
        self.x = x+offset
        self.y = y+offset
        self.image = image
        self.image_selected = image_selected
        self.selected = False
        self.select_radius = select_radius


# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
DISPLAY_HEIGHT = 600
SCREEN_HEIGHT = 600+100
TILE_SIZE = 50  # Size of each hexagon tile
CENTER = (SCREEN_WIDTH/2, DISPLAY_HEIGHT/2)

# Colors
WHITE = (255, 255, 255)
GREEN = (50, 220, 50)
BLUE_D = (100, 100, 200)
BLACK = (0, 0, 0)
GRAY_BROWN = (172,157,129)
YELLOW = (200,200,50)

# positive directions are y: up, x, up-right
# but as the hexagon has 6 sides, some re-defining needs to be made
directions = [(0, 1), (1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1)]

# Terrain
hills = pygame.transform.scale(pygame.image.load("hills.png"), (100, 100))
forest = pygame.transform.scale(pygame.image.load("forest.png"), (100, 100))
empty = pygame.transform.scale(pygame.image.load("empty.png"), (100, 100))

# Units
warrior = pygame.transform.scale(pygame.image.load("warrior.png"), (60, 60))
archer = pygame.transform.scale(pygame.image.load("archer.png"), (60, 60))

# Action bar buttons
move = pygame.transform.scale(pygame.image.load("move.png"), (60, 60))
target = pygame.transform.scale(pygame.image.load("target.png"), (60, 60))
fortify = pygame.transform.scale(pygame.image.load("fortify.png"), (60, 60))
move_s = pygame.transform.scale(pygame.image.load("move_selected.png"), (60, 60))
target_s = pygame.transform.scale(pygame.image.load("target_selected.png"), (60, 60))
fortify_s = pygame.transform.scale(pygame.image.load("fortify_selected.png"), (60, 60))

button_list = [Button(560, 620, move, move_s, 30, 30),
               Button(630, 620, target, target_s, 30, 30),
               Button(700, 620, fortify, fortify_s, 30, 30)]


terrains_dict = {0: empty, 1: hills, 2: forest}
movement_costs = {0: 1, 1: 2, 2: 2}


class Square:
    def __init__(self, x, y, size, terrain, board_center, index):
        self.x = x
        self.y = y
        self.size = size
        self.terrain = terrain
        # terrains: 0 = plains, 1 = hills, 2 = forest, 3 = forest and hills, 4 = water
        self.unit = None

        self.center = (np.cos(np.pi/6)*2*x*size*np.sin(np.pi/3), np.cos(np.pi/6)*(y + x*np.cos(np.pi/3))*2*size)
        self.movement_cost = movement_costs[self.terrain]
        self.index = index


# warrior: 2 movement, melee
class Unit:
    def __init__(self, type, location):
        self.type = type
        self.health = 100
        self.attack = 20
        self.movement_max = 2
        self.movement_left = self.movement_max
        self.location = location
        self.image = warrior

        self.fortified = False

        self.ranged = False
        self.range = 0


def check_for_button_clicked(button: Button, click_location):
    """
    Checks if click is within [radius] pixels from the click location
    :param button: Button
    :param click_location: (int, int)
    :return: Bool
    """
    if math.sqrt(math.pow(button.x-click_location[0], 2) + math.pow(button.y-click_location[1], 2)) < button.select_radius:
        return True
    else:
        return False


def draw_action_bar(surface, buttons: list[Button]):
    pygame.draw.polygon(surface, BLUE_D, [[0, 600], [800, 600], [800, 700], [0, 700]])
    for button in buttons:
        if button.selected:
            surface.blit(button.image_selected, (button.x-30, button.y-30))
        else:
            surface.blit(button.image, (button.x-30, button.y-30))
    '''surface.blit(move, (560, 620))
    surface.blit(target, (630, 620))
    surface.blit(fortify, (700, 620))'''



def move_unit(unit, sq_from, sq_to):
    """
    Moves a unit from one square to another
    :param unit: Unit
    :param sq_from: Square
    :param sq_to: Square
    :return: None
    """
    sq_from.unit = None
    sq_to.unit = unit


def are_neighbors(s1: Square, s2: Square):
    """
    Checks, weather squares are adjacent to each other
    :param s1: square
    :param s2: square
    :return: Bool
    """
    return (s1.x-s2.x, s1.y-s2.y) in directions


def square_by_coordinates(squares, x, y):
    """
    Returns the square with coordinates x,y
    :param squares: list[Square]
    :param x: int
    :param y: int
    :return: Square
    """
    for square in squares:
        if square.x == x and square.y == y:
            return square

def get_neighbors(s: Square, squares: list[Square]):
    """
    Gets the neighbors of a square
    :param s: square
    :return: list[square]
    """
    neighbor_coordinates = [(s.x+d[0], s.y+d[1]) for d in directions]
    return [square_by_coordinates(squares, x, y) for x, y in neighbor_coordinates if square_by_coordinates(squares, x, y)]

def get_neighbor_indices(s: Square, squares: list[Square]):
    """
    Gets the indices of the neighboring squares
    :param s: square
    :return: list[square]
    """
    neighbor_coordinates = [(s.x+d[0], s.y+d[1]) for d in directions]
    return [square_by_coordinates(squares, x, y).index for x, y in neighbor_coordinates if square_by_coordinates(squares, x, y)]

def create_board(amount: int, size: float):
    """
    Creates a hexagon shaped board, whose diameter is 1+2*amount hexes
    :param amount:
    :param size:
    :return: list[square]
    """
    hexes = [Square(0,0,50, 1, CENTER, 0)]
    tot = 0
    for i in range(amount):
        for dir in range(len(directions)):
            for j in range(i+1):
                tot += 1
                x = (i+1)*directions[dir][0] + j*directions[(dir-2)%6][0]
                y = (i+1)*directions[dir][1] + j*directions[(dir-2)%6][1]
                ter = random.choices([0, 1, 2], weights=[2, 1, 1])[0]
                hexes.append(Square(x, y, size, ter, CENTER, tot))
    return hexes


# Function to draw a hexagon
def draw_hexagon(surface, sq: Square, center: (int, int)):
    """
    Draws a single hexagon using information from the square-class and
    information about the surface
    :param surface:
    :param sq: square
    :param center: (int, int)
    :return: None
    """
    x = sq.x
    y = sq.y
    size = sq.size
    type = sq.terrain
    angle = np.pi/3
    points = []
    for i in range(6):
        x_i = x + size * math.cos(angle * i) + sq.center[0] + center[0]
        y_i = y + size * math.sin(angle * i) + sq.center[1] + center[1]
        points.append((x_i, y_i))
    pygame.draw.polygon(surface, GREEN, points)
    pygame.draw.polygon(surface, WHITE, points, 2)

    surface.blit(terrains_dict[type], (sq.center[0]+center[0]-50, sq.center[1]+center[1]-50))
    if sq.unit:
        surface.blit(sq.unit.image, (sq.center[0]+center[0]-30, sq.center[1]+center[1]-30))


def highlight_hexagon(surface, sq: Square, center: (int, int)):
    """
    Highlights a single hexagon
    :param surface:
    :param sq: Square
    :param center: (int, int)
    :return: None
    """
    x = sq.x
    y = sq.y
    size = sq.size
    angle = np.pi/3
    points = []
    for i in range(6):
        x_i = x + size * math.cos(angle * i) + sq.center[0] + center[0]
        y_i = y + size * math.sin(angle * i) + sq.center[1] + center[1]
        points.append((x_i, y_i))
    pygame.draw.polygon(surface, YELLOW, points, 6)


def pathfinding(start: Square, end: Square, squares: list[Square]):
    """
    A really basic pathfinding algorithm, return movement cost
    TODO: improve efficiency
    :param start: Square
    :param end: Square
    :param squares:
    :return: int
    """
    previously_visited_og = {start.index: 0}
    previously_visited = copy.deepcopy(previously_visited_og)

    def expand():
        for key, value in previously_visited_og.items():
            neighbors = get_neighbor_indices(hexagons[key], squares)
            for neighbor in neighbors:
                if neighbor in previously_visited:
                    if value + hexagons[neighbor].movement_cost < previously_visited[neighbor]:
                        previously_visited[neighbor] = value + hexagons[neighbor].movement_cost
                else:
                    previously_visited[neighbor] = value + hexagons[neighbor].movement_cost
    while end.index not in previously_visited:
        expand()
        previously_visited_og = copy.deepcopy(previously_visited)
    for i in range(3):
        expand()
        previously_visited_og = copy.deepcopy(previously_visited)
    return previously_visited[end.index]


def new_turn(board: list[Square]):
    """
    Heals units and refreshes their movement
    :param board:
    :return:
    """
    for sq in board:
        if not sq.unit:
            continue
        if sq.unit.movement_left == sq.unit.movement_max:
            sq.unit.health = min(100, sq.unit.health+10)
        sq.unit.movement_left = sq.unit.movement_max


# Function to draw the hexagon board
def draw_hexagon_board(surface, squares: list[Square]):
    """
    Loops through the hexagons and individually draws them
    :param surface:
    :param squares: list[square]
    :return: None
    """
    for sq in squares:
        draw_hexagon(surface, sq, (400, 300))


def click_square(x: float, y: float, center: (int, int), hexes: list[Square]):
    """
    returns the square clicked
    :param x:
    :param y:
    :param center:
    :param list[Square]:
    :return: Square
    """
    distances = [(np.sqrt(math.pow(hexes[i].center[0]+center[0]-x, 2) + math.pow(hexes[i].center[1]+center[1]-y, 2)),i) for i in range(len(hexes))]
    distances.sort()
    if distances[0][0] < 60:
        return distances[0][1]
    else:
        return None


def unselect_buttons(buttons: list[Button]):
    for button in buttons:
        button.selected = False


hexagons = create_board(2, 50)
# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Hexagon Board')


# MANUALLY ADD UNITS HERE
hexagons[9].unit = Unit(1, (hexagons[9].x, hexagons[9].y))
hexagons[15].unit = Unit(1, (hexagons[15].x, hexagons[15].y))

selected_hex = None

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            button_clicked = False
            x, y = event.pos
            # Check if a button was clicked
            for i, but in enumerate(button_list):
                if check_for_button_clicked(but, (x, y)):
                    unselect_buttons(button_list)
                    button_clicked = True
                    button_list[i].selected = True
            # Check which hexagon was clicked (if any)
            if not button_clicked:
                new_selection = (click_square(x, y, (400, 300), hexagons))

                # Check if unit should be moved
                if selected_hex is not None and new_selection is not None:
                    if button_list[0].selected:
                        # check if enough movement
                        movement_required = pathfinding(hexagons[selected_hex], hexagons[new_selection], hexagons)
                        if hexagons[selected_hex].unit.movement_left >= movement_required:
                            hexagons[selected_hex].unit.movement_left -= movement_required
                            move_unit(hexagons[selected_hex].unit, hexagons[selected_hex], hexagons[new_selection])
                        else:
                            print("not enough movement")

                # unselect action
                if new_selection is None or new_selection != selected_hex:
                    unselect_buttons(button_list)
                selected_hex = new_selection

    screen.fill(GRAY_BROWN)

    draw_hexagon_board(screen, hexagons)

    draw_action_bar(screen, button_list)

    # Highlights a selected hexagon
    if selected_hex is not None:
        highlight_hexagon(screen, hexagons[selected_hex], CENTER)

    pygame.display.flip()


