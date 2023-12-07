"""

The part of the program that represents the game
non-visually

"""
import numpy as np
import random

from units import Unit, create_unit

movement_costs = {0: 1, 1: 2, 2: 2, 3: 3, 4: 2, 5: -1, 6: -1}
terrain_combat_modifier = {0: 0, 1: 3, 2: 3, 3: 6, 4: -3}
directions = [(0, 1), (1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1)]
directions2 = [(0, 1), (1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1),
               (0, 2), (2, 0), (2, -2), (0, -2), (-2, 0), (-2, 2),
               (1, 1), (2, -1), (1, -2), (-1, -1), (-2, 1), (-1, 2)]


SCREEN_WIDTH = 800
DISPLAY_HEIGHT = 600
SCREEN_HEIGHT = 600+100
TILE_SIZE = 50
CENTER = (SCREEN_WIDTH/2, DISPLAY_HEIGHT/2)


class Teams:
    def __init__(self, teams: list[list[Unit]]):
        self.teams = teams

    def get_team(self, index: int):
        return self.teams[index]


class Turns:
    def __init__(self, no_players: int):
        self.turn = 0
        self.to_play = 0
        self.no_players = no_players

    def next_player(self):
        if self.to_play == self.no_players - 1:
            self.turn += 1
            self.to_play = 0
        else:
            self.to_play += 1


class Square:
    def __init__(self, x: int, y: int, terrain: int, index: int):
        self.x = x
        self.y = y
        self.terrain = terrain
        self.unit = None

        self.movement_cost = movement_costs[self.terrain]
        self.index = index
        self.center = (CENTER[0] + np.cos(np.pi/6)*2*self.x*TILE_SIZE*np.sin(np.pi/3),
                       CENTER[1] + np.cos(np.pi/6)*(self.y + self.x*np.cos(np.pi/3))*2*TILE_SIZE)



# helper functions
def square_by_coordinates(squares: list[Square], x: int, y: int):
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

def get_neighbors(square: Square, squares: list[Square], range=1):
    """
    Gets the neighbors of a square
    :param square:
    :param squares:
    :param range:
    :return:
    """
    if range == 1:
        neighbor_coordinates = [(square.x + d[0], square.y + d[1]) for d in directions]
        return [square_by_coordinates(squares, x, y) for x, y in neighbor_coordinates if
                square_by_coordinates(squares, x, y)]
    elif range == 2:
        neighbor_coordinates = [(square.x + d[0], square.y + d[1]) for d in directions2]
        return [square_by_coordinates(squares, x, y) for x, y in neighbor_coordinates if
                square_by_coordinates(squares, x, y)]



def create_board(amount: int):
    """
    Creates a hexagon shaped board, whose diameter is 1+2*amount hexes
    :param amount: int
    :return: list[square]
    """
    first_terrain = random.choices([0, 1, 2, 3, 4, 5, 6], weights=[6, 2, 2, 2, 1, 0.5, 1])[0]
    hexes = [Square(0,0,first_terrain, 0)]
    tot = 0
    for i in range(amount):
        for dir in range(len(directions)):
            for j in range(i+1):
                tot += 1
                x = (i+1)*directions[dir][0] + j*directions[(dir-2)%6][0]
                y = (i+1)*directions[dir][1] + j*directions[(dir-2)%6][1]
                ter = random.choices([0, 1, 2, 3, 4, 5, 6], weights=[6, 2, 2, 2, 1, 0.5, 1])[0]
                hexes.append(Square(x, y, ter, tot))
    return hexes

class Game:
    def __init__(self, no_players: int, board_size: int):
        self.squares: list[Square] = create_board(board_size)
        self.teams = []
        self.turns = Turns(no_players)
        # precalculate neighbors for each square, as they will be needed often
        self.index_to_neighbors = {}
        self.coordinates_to_neighbor = {}
        self.coordinates_to_square = {}
        for square in self.squares:
            self.index_to_neighbors[square.index] = get_neighbors(square, self.squares)
            self.coordinates_to_neighbor[(square.x, square.y)] = get_neighbors(square, self.squares)
            self.coordinates_to_square[(square.x, square.y)] = square

    # Update the board
    def defence_modifier(self, defender: Square, melee=True):
        modifier = 0
        # unit health
        modifier -= round(10 - defender.unit.health / 10)
        # terrain
        modifier += terrain_combat_modifier[defender.terrain]
        # fortifying
        if defender.unit.fortified:
            modifier += 6
        # support
        if melee:
            neighbors = self.index_to_neighbors[defender.index]
            for neighbor in neighbors:
                if neighbor.unit and neighbor.unit.team == defender.unit.team:
                    modifier += 2
        return modifier

    def offence_modifier(self, attacker: Square, defender: Square, melee=True):
        modifier = 0
        # unit health
        modifier -= round(10 - attacker.unit.health / 10)
        if melee:
            # flanking
            # let's assume all teams are always at war with each other
            defender_neighbors = self.index_to_neighbors[defender.index]
            for neighbor in defender_neighbors:
                if neighbor.unit and neighbor.unit.team != defender.unit.team:
                    modifier += 2
            modifier -= 2  # the attacker should not count into flanking bonus
        return modifier

    def ranged_combat(self, attacker: Square, defender: Square):
        strength_difference = ((attacker.unit.ranged_strength + self.offence_modifier(attacker, defender, False)) -
                               (defender.unit.strength + self.defence_modifier(defender, False)))
        attacker.unit.fortified = False
        attacker.unit.movement_left = 0
        defender.unit.health = round(defender.unit.health - 30 * np.exp(strength_difference / 25))
        if defender.unit.health <= 0:
            defender.unit = None

    def melee_combat(self, attacker: Square, defender: Square):
        attacker.unit.movement_left = 0
        strength_difference = ((attacker.unit.strength + self.offence_modifier(attacker, defender)) -
                               (defender.unit.strength + self.defence_modifier(defender)))

        attacker.unit.health = round(attacker.unit.health - 30 * np.exp(-strength_difference / 25))
        defender.unit.health = round(defender.unit.health - 30 * np.exp(strength_difference / 25))
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

    def move_unit(self, start_coords: (int, int), end_coords: (int, int), movement_cost: int):
        """
        Moves a unit from one square to another
        :param start_coords:
        :param end_coords:
        :return:
        """
        square_start = self.coordinates_to_square[start_coords]
        square_end = self.coordinates_to_square[end_coords]
        square_start.unit.fortified = False
        square_start.unit.movement_left -= movement_cost
        square_end.unit = square_start.unit
        square_start.unit = None

    def update_state(self, start_coordinates: (int, int), end_coordinates: (int, int),
                     previous_square_coordinates: (int, int), movement_cost: int, move=True):
        start = self.coordinates_to_square[start_coordinates]
        end = self.coordinates_to_square[end_coordinates]
        if move:
            if end.unit:
                self.move_unit(start_coordinates, previous_square_coordinates, movement_cost)
                self.melee_combat(start, end)
            else:
                self.move_unit(start_coordinates, end_coordinates, movement_cost)
        else:
            self.ranged_combat(end, start)

    def end_turn(self):
        """
        Heals units and refreshes their movement
        Fortifies unit if still has full movement
        :param board:
        :return:
        """
        for sq in self.squares:
            if not sq.unit:
                continue
            if sq.unit.team != self.turns.to_play:
                continue
            if sq.unit.movement_left == sq.unit.movement_max:
                sq.unit.health = min(100, sq.unit.health + 10)
                sq.unit.fortified = True
            sq.unit.movement_left = sq.unit.movement_max
        self.turns.next_player()


    # RL components
    def get_action_space(self):
        pass

    def get_game_state(self):
        pass

    def get_reward(self):
        pass




game = Game(2, 3)

"""
note to self
the communication between logic and AI:
possible actions is called
    actions are stored in format (start, end, previous, movement_cost, move=Bool)
    actually all of the should probably be passed to AI

"""
