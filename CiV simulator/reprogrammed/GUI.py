from gameLogic import Game, Turns, Square, Teams
from gameLogic import movement_costs, terrain_combat_modifier, game
from units import Unit
import pygame
import sys
import math
import numpy as np


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


def draw_action_bar():
    # draw buttons
    pass


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Hexagon Board')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        draw_board(game, screen)
        pygame.display.flip()


