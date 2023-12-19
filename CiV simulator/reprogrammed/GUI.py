from gameLogic import Game, Turns, Square#, Teams
from gameLogic import movement_costs, terrain_combat_modifier, game
from units import Unit
import pygame
import sys
import math
import numpy as np


pygame.init()

class Button:
    #__slots__ = ("image", "image_selected", "select_radius", "x", "y")
    def __init__(self, x, y, image, image_selected, select_radius, offset):
        self.x = x+offset
        self.y = y+offset
        self.image = image
        self.image_selected = image_selected
        self.selected = False
        self.select_radius = select_radius

SCREEN_WIDTH = 800
DISPLAY_HEIGHT = 600
SCREEN_HEIGHT = 600+100
TILE_SIZE = 50
CENTER = (SCREEN_WIDTH/2, DISPLAY_HEIGHT/2)
# Colors
WHITE = (255, 255, 255)
GREEN = (50, 220, 50)
GREEN_D = (50, 140, 50)
BLUE_D = (100, 100, 200)
RED = (150, 50, 50)
BLACK = (0, 0, 0)
GRAY_BROWN = (172,157,129)
DARKER_BROWN = (142,137,119)
YELLOW = (200,200,50)

# Terrain
empty = pygame.transform.scale(pygame.image.load("empty.png"), (100, 100))
hills = pygame.transform.scale(pygame.image.load("hills.png"), (100, 100))
forest = pygame.transform.scale(pygame.image.load("forest.png"), (100, 100))
hills_and_forest = pygame.transform.scale(pygame.image.load("hills_and_forest.png"), (100, 100))
marsh = pygame.transform.scale(pygame.image.load("marsh.png"), (100, 100))
ocean = pygame.transform.scale(pygame.image.load("ocean.png"), (100, 100))
mountain = pygame.transform.scale(pygame.image.load("mountain.png"), (100, 100))

terrains_dict = {0: empty, 1: hills, 2: forest, 3: hills_and_forest, 4: marsh, 5: ocean, 6: mountain}

# Action bar buttons
move = pygame.transform.scale(pygame.image.load("move.png"), (60, 60))
target = pygame.transform.scale(pygame.image.load("target.png"), (60, 60))
fortify = pygame.transform.scale(pygame.image.load("fortify.png"), (60, 60))
end_turn = pygame.transform.scale(pygame.image.load("end_turn.png"), (80, 80))

move_s = pygame.transform.scale(pygame.image.load("move_selected.png"), (60, 60))
target_s = pygame.transform.scale(pygame.image.load("target_selected.png"), (60, 60))
fortify_s = pygame.transform.scale(pygame.image.load("fortify_selected.png"), (60, 60))
end_turn_s = pygame.transform.scale(pygame.image.load("end_turn_selected.png"), (80, 80))

button_list = [Button(460, 620, move, move_s, 30, 30),
               Button(530, 620, target, target_s, 30, 30),
               Button(600, 620, fortify, fortify_s, 30, 30),
               Button(690, 600, end_turn, end_turn_s, 40, 40)]

font_small = pygame.font.Font(None, 18)


def draw_board(game: Game, surface):
    def draw_square(sq: Square):
        """
        Draws a single hexagon and possibly unit on it using information from the square-class and
        information about the surface
        :param game: Game
        :param sq: square
        :return: None
        """
        x = sq.x
        y = sq.y
        type = sq.terrain
        angle = np.pi / 3
        points = []
        for i in range(6):
            x_i = x + TILE_SIZE * math.cos(angle * i) + sq.center[0]
            y_i = y + TILE_SIZE * math.sin(angle * i) + sq.center[1]
            points.append((x_i, y_i))
        if sq.terrain == 5:
            pygame.draw.polygon(surface, BLUE_D, points)
        else:
            pygame.draw.polygon(surface, GREEN, points)
            pygame.draw.polygon(surface, GREEN_D, points, 1)

        surface.blit(terrains_dict[type], (sq.center[0] - 50, sq.center[1] - 50))
        if sq.unit:
            if sq.unit.fortified:
                surface.blit(sq.unit.image_fortified, (sq.center[0] - 30, sq.center[1] - 30))
            else:
                surface.blit(sq.unit.image, (sq.center[0] - 30, sq.center[1] - 30))

    for square in game.squares:
        draw_square(square)


def draw_action_bar(surface):
    pygame.draw.polygon(surface, BLUE_D, [[0, 600], [800, 600], [800, 700], [0, 700]])
    for button in button_list:
        if button.selected:
            surface.blit(button.image_selected, (button.x-30, button.y-30))
        else:
            surface.blit(button.image, (button.x-30, button.y-30))

# CLICK DETECTION

def get_square_clicked(x: float, y: float, squares: list[Square]):
    """
    returns the square clicked
    :param x:
    :param y:
    :param center:
    :param list[Square]:
    :return int: square index
    """
    distances = [(
        np.sqrt(math.pow(squares[i].center[0]-x, 2) +
                math.pow(squares[i].center[1]-y, 2)),
        i
    ) for i in range(len(squares))]
    distances.sort()
    if distances[0][0] < 60:
        return distances[0][1]
    else:
        return None


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


def highlight_square(surface, sq: Square, color=YELLOW):
    """
    Highlights a single hexagon
    :param surface:
    :param sq: Square
    :param center: (int, int)
    :return: None
    """
    x = sq.x
    y = sq.y
    angle = np.pi/3
    points = []
    for i in range(6):
        x_i = x + TILE_SIZE * math.cos(angle * i) + sq.center[0]
        y_i = y + TILE_SIZE * math.sin(angle * i) + sq.center[1]
        points.append((x_i, y_i))
    pygame.draw.polygon(surface, color, points, 6)


def unselect_buttons():
    for button in button_list:
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


def display_actions(surface, action_space: list, unit: Unit):
    for act in action_space:
        if act[0] == unit.location:

            highlight_square(surface, game.coordinates_to_square[act[1]], color=BLUE_D)


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Hexagon Board')

actions = game.get_action_space()


previous_selection = None
current_selection = None

while True:
    for event in pygame.event.get():
        screen.fill(GRAY_BROWN)
        button_clicked = False
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            # Check is button clicked
            for i, but in enumerate(button_list):
                if check_for_button_clicked(but, (x, y)):
                    unselect_buttons()
                    button_clicked = True
                    button_list[i].selected = True

            # Otherwise check if square is clicked
            if not button_clicked:
                previous_selection = current_selection
                current_selection = get_square_clicked(x, y, game.squares)
                # Check if action should be performed in game
                # move
                if button_list[0].selected:
                    if current_selection is not None and previous_selection is not None:
                        prev, cur = game.squares[previous_selection].loc, game.squares[current_selection].loc
                        for action in actions:
                            if action[4]:
                                if action[0] == prev and action[1] == cur:
                                    game.perform_action(*action)
                                    current_selection, previous_selection = None, None
                                    actions = game.get_action_space()
                # ranged attack
                if button_list[1].selected:
                    if current_selection is not None and previous_selection is not None:
                        prev, cur = game.squares[previous_selection].loc, game.squares[current_selection].loc
                        for action in actions:
                            if not action[4]:
                                if action[0] == prev and action[1] == cur:
                                    game.perform_action(*action)
                                    current_selection, previous_selection = None, None
                                    actions = game.get_action_space()
                # end turn
                if button_list[3].selected:
                    game.perform_action(0)
                    unselect_buttons()
                    actions = game.get_action_space()

        draw_board(game, screen)
        draw_action_bar(screen)

        if current_selection is not None:
            # and display stats
            if game.squares[current_selection].unit:
                display_stats(screen, game.squares[current_selection].unit)
                display_actions(screen, actions, game.squares[current_selection].unit)
            highlight_square(screen, game.squares[current_selection])



        pygame.display.flip()



# TODO: check out gymnasium
