import copy
import pygame
import sys
import math
import numpy as np
import random

from units import Unit, create_unit

"""
The goal is to create rules to play a bit of Civilization
More specifically, this program aims to be a small-scale 
battle simulator for 2+ units.
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
DARKER_BROWN = (142,137,119)
YELLOW = (200,200,50)

font_small = pygame.font.Font(None, 18)

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


def change_color(image_path: str, color: (int, int, int, int)):
    img = pygame.transform.scale(pygame.image.load(image_path), (60, 60))
    for x in range(img.get_width()):
        for y in range(img.get_height()):
            pixel_color = img.get_at((x, y))
            if pixel_color == (0, 0, 0, 255):  # Check if the pixel is black
                img.set_at((x, y), color)  # Change to blue
    return img


warrior_blue = change_color("warrior.png", (100, 100, 200, 255))
warrior_red = change_color("warrior.png", (200, 50, 50, 255))
warrior_list = [warrior_blue, warrior_red]
# TODO: make above process a function

# Action bar buttons
move = pygame.transform.scale(pygame.image.load("move.png"), (60, 60))
target = pygame.transform.scale(pygame.image.load("target.png"), (60, 60))
fortify = pygame.transform.scale(pygame.image.load("fortify.png"), (60, 60))
end_turn = pygame.transform.scale(pygame.image.load("end_turn.png"), (80, 80))

move_s = pygame.transform.scale(pygame.image.load("move_selected.png"), (60, 60))
target_s = pygame.transform.scale(pygame.image.load("target_selected.png"), (60, 60))
fortify_s = pygame.transform.scale(pygame.image.load("fortify_selected.png"), (60, 60))

button_list = [Button(460, 620, move, move_s, 30, 30),
               Button(530, 620, target, target_s, 30, 30),
               Button(600, 620, fortify, fortify_s, 30, 30),
               Button(690, 600, end_turn, end_turn, 40, 40)]


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
    iteratively find squares accecible by 0, 1, 2... moves.
    when new squares are found, they are added to the list
    algo ends when destination is first reached
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


def combat_melee(attacker: Square, defender: Square):
    attacker.unit.movement_left = 0
    strength_difference = attacker.unit.strength - defender.unit.strength
    attacker.unit.health = round(attacker.unit.health-30*np.exp(-strength_difference/25))
    defender.unit.health = round(defender.unit.health-30*np.exp(strength_difference/25))
    # if both "die", only the one that dies more really dies
    if attacker.unit.health <= 0 and defender.unit.health <= 0:
        if attacker.unit.health > defender.unit.health:
            attacker.unit.health = 1
            defender.unit.health = 0
        else:
            attacker.unit.health = 0
            defender.unit.health = 1
    # if attacker dies
    if attacker.unit.health <= 0:
        attacker.unit = None
    # if defender dies
    if defender.unit.health <= 0:
        defender.unit = attacker.unit
        defender.unit.movement_left = 0
        attacker.unit = None


def unselect_buttons(buttons: list[Button]):
    for button in buttons:
        button.selected = False


def display_stats(surface, unit: Unit):
    pygame.draw.polygon(surface, DARKER_BROWN, [[0, 600], [250, 600], [250, 700], [0, 700]])
    surface.blit(unit.image, (20, 620))

    def draw_text(text, size, x, y, color=BLACK):
        font = pygame.font.SysFont("comicsans", size)
        label = font.render(text, 1, color)
        surface.blit(label, (x, y))

    draw_text("Health: ", 18, 100, 620)
    draw_text("Movement: ", 18, 100, 645)
    draw_text("Strength: ", 18, 100, 670)

    draw_text(str(unit.health), 18, 200, 620)
    draw_text(str(unit.movement_left) + "/" + str(unit.movement_max), 18, 200, 645)
    draw_text(str(unit.strength), 18, 200, 670)


hexagons = create_board(2, 50)
# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Hexagon Board')


# MANUALLY ADD UNITS HERE
hexagons[9].unit = create_unit("chariot", (hexagons[9].x, hexagons[9].y), 1)
hexagons[15].unit = create_unit("swordsman", (hexagons[15].x, hexagons[15].y), 2)

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
                        # TODO: if full movement, can always move one
                        movement_required = pathfinding(hexagons[selected_hex], hexagons[new_selection], hexagons)
                        if hexagons[selected_hex].unit.movement_left >= movement_required:
                            # check if initiates combat
                            if hexagons[new_selection].unit:
                                if hexagons[selected_hex].unit.team != hexagons[new_selection].unit.team:
                                    combat_melee(hexagons[selected_hex], hexagons[new_selection])
                            else:
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
        # and display stats
        if hexagons[selected_hex].unit:
            display_stats(screen, hexagons[selected_hex].unit)

    # If end turn is chosen
    if button_list[3].selected:
        unselect_buttons(button_list)
        new_turn(hexagons)

    pygame.display.flip()


