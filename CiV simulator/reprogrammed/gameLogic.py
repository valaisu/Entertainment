"""

The part of the program that represents the game
non-visually

"""
import numpy as np


from units import Unit, create_unit


movement_costs = {0: 1, 1: 2, 2: 2, 3: 3, 4: 2, 5: -1, 6: -1}
terrain_combat_modifier = {0: 0, 1: 3, 2: 3, 3: 6, 4: -3}


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

    def center(self, hexagon_size: float, board_center: (int, int)):
        return (board_center[0] + np.cos(np.pi/6)*2*self.x*hexagon_size*np.sin(np.pi/3),
                board_center[1] + np.cos(np.pi/6)*(self.y + self.x*np.cos(np.pi/3))*2*hexagon_size)
    # above maybe should be evaluated just once, this can be done in the GUI


class Game:
    def __init__(self, no_players: int):
        self.squares: list[Square] = []
        self.teams = []
        self.turns = Turns(no_players)

    #Initialise the board


    #Update the board
    def defence_modifier(self, attacker: Square, defender: Square):
        pass

    def offence_modifier(self, attacker: Square, defender: Square):
        pass

    def ranged_combat(self, attacker: Square, defender: Square):
        pass

    def melee_combat(self, attacker: Square, defender: Square):
        pass

    def move_unit(self, square_start: Square, square_end: Square, movement_cost: int):
        pass

    def update_state(self, square_start: int, square_end: int, previous_square: int, move=True):
        pass

    def end_turn(self):
        pass


    # RL components
    def get_action_space(self):
        pass

    def get_game_state(self):
        pass

    def get_reward(self):
        pass


