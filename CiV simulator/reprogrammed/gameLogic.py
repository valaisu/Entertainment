"""

The part of the program that represents the game
non-visually

"""

'''
ideas to improve efficiency 
    keep register of unit locations
'''

import numpy as np
import random

from units import Unit, create_unit

movement_costs = {0: 1, 1: 2, 2: 2, 3: 3, 4: 2, 5: -1, 6: -1}
terrain_combat_modifier = {0: 0, 1: 3, 2: 3, 3: 6, 4: -3}
#terrains_dict = {0: empty, 1: hills, 2: forest, 3: hills_and_forest, 4: marsh, 5: ocean, 6: mountain}
terrain_elevation = {0: 0, 1: 1, 2: 1, 3: 2, 4: 0, 5: 0, 6: 3}
directions = [(0, 1), (1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1)]
directions2 = [(0, 1), (1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1),
               (0, 2), (2, 0), (2, -2), (0, -2), (-2, 0), (-2, 2),
               (1, 1), (2, -1), (1, -2), (-1, -1), (-2, 1), (-1, 2)]

# below tells which squares might block sight to which
obstacles = \
    {(0, 2): [(0, 1)], (2, 0): [(1, 0)], (2, -2): [(1, -1)], (0, -2): [(0, -1)], (-2, 0): [(-1, 0)], (-2, 2): [(-1, 1)],
     (1, 1): [(0, 1), (1, 0)], (2, -1): [(1, -1), (1, 0)], (1, -2): [(0, -1), (1, -1)], (-1, -1): [(-1, 0), (0, -1)]}

SCREEN_WIDTH = 800
DISPLAY_HEIGHT = 600
SCREEN_HEIGHT = 600+100
TILE_SIZE = 50
CENTER = (SCREEN_WIDTH/2, DISPLAY_HEIGHT/2)


'''class Teams:
    def __init__(self, teams: list[list[Unit]]):
        self.teams = teams

    def get_team(self, index: int):
        return self.teams[index]
'''

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
        self.loc = (x, y)
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


def get_neighbors_index(square: Square, squares: list[Square], range=1):
    """
    Gets the neighbors of a square
    :param square:
    :param squares:
    :param range:
    :return:
    """
    if range == 1:
        neighbor_coordinates = [(square.x + d[0], square.y + d[1]) for d in directions]
        return [square_by_coordinates(squares, x, y).index for x, y in neighbor_coordinates if
                square_by_coordinates(squares, x, y)]
    elif range == 2:
        neighbor_coordinates = [(square.x + d[0], square.y + d[1]) for d in directions2]
        return [square_by_coordinates(squares, x, y).index for x, y in neighbor_coordinates if
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
        #self.teams = []
        self.turns = Turns(no_players)
        # precalculate neighbors for each square, as they will be needed often
        self.index_to_neighbors = {}
        self.index_to_square = {}
        self.coordinates_to_neighbor = {}
        self.coordinates_to_square = {}
        for square in self.squares:
            self.index_to_neighbors[square.index] = get_neighbors(square, self.squares)
            self.index_to_square[square.index] = square
            #self.index_to_neighbors[square.index] = [self.squares[sq] for sq in get_neighbors_index(square, self.squares)]
            # THE GET NEIGHBORS IS A FUNCTION OUTSIDE OF THE CLASS
            # AND THEREFOR CREATES A NON-SHALLOW COPY OF THE NEIGHBORS
            self.coordinates_to_neighbor[(square.x, square.y)] = [self.squares[sq] for sq in get_neighbors_index(square, self.squares)]
            self.coordinates_to_square[(square.x, square.y)] = square
        '''        
        for i in range(len(self.squares)):
            self.index_to_neighbors[self.squares[i].index] = get_neighbors(self.squares[i], self.squares)
            self.coordinates_to_neighbor[(self.squares[i].x, self.squares[i].y)] = get_neighbors(self.squares[i], self.squares)
            self.index_to_square[self.squares[i].index] = self.squares[i]
            self.coordinates_to_square[(self.squares[i].x, self.squares[i].y)] = self.squares[i]'''

    def set_units_on_board(self, team1: list[str], team2: list[str], sq1: int = 31, sq2: int = 22):
        """
        Generates two armies around squares 31/sq1 and 22/sq2
        :param team1: list[str]
        :param team2: list[str]
        :param sq1: int
        :param sq2: int
        :return: None
        """
        team1_units = []
        valid_squares_1 = []
        if self.squares[sq1].terrain not in [5, 6]:
            valid_squares_1.append(sq1)
            self.squares[sq1].unit = create_unit(team1[0], (self.squares[sq1].x, self.squares[sq1].y), 0)
            team1_units.append(self.squares[sq1].unit)
        queue1 = get_neighbors(self.squares[sq1], self.squares, 2)
        counter = 0
        while len(valid_squares_1) < len(team1):
            ind = queue1[counter].index
            if self.squares[ind].terrain not in [5, 6]:
                valid_squares_1.append(ind)
                self.squares[ind].unit = create_unit(team1[len(valid_squares_1) - 1], (self.squares[ind].x, self.squares[ind].y), 0)
                team1_units.append(self.squares[ind].unit)
            counter += 1

        team2_units = []
        valid_squares_2 = []
        if self.squares[sq2].terrain not in [5, 6]:
            valid_squares_2.append(sq2)
            self.squares[sq2].unit = create_unit(team2[0], (self.squares[sq2].x, self.squares[sq2].y), 1)
            team2_units.append(self.squares[sq2].unit)
        queue2 = get_neighbors(self.squares[sq2], self.squares, 2)
        counter = 0
        while len(valid_squares_2) < len(team2):
            ind = queue2[counter].index
            if self.squares[ind].terrain not in [5, 6]:
                valid_squares_2.append(ind)
                self.squares[ind].unit = create_unit(team2[len(valid_squares_2) - 1], (self.squares[ind].x, self.squares[ind].y), 1)
                team2_units.append(self.squares[ind].unit)
            counter += 1

        #self.teams = [team1_units, team2_units]
        #print(self.teams)

    #def update_unit_loc(self, unit: Unit):


    def get_team(self, team: int):
        team_units = []
        for square in self.squares:
            if square.unit:
                print(square.unit.team, team)
            if square.unit and square.unit.team == team:
                team_units.append(square.unit)
        return team_units

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
            defender.unit.location = defender.loc
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
        square_end.unit.location = square_end.loc
        square_start.unit = None

    def update_state(self, start_coordinates: (int, int), end_coordinates: (int, int),
                     previous_square_coordinates: (int, int), movement_cost: int, move: bool):
        start = self.coordinates_to_square[start_coordinates]
        prev = self.coordinates_to_square[previous_square_coordinates]
        end = self.coordinates_to_square[end_coordinates]
        print("indices: ", start.index, prev.index, end.index)
        if move:
            if end.unit:
                if start!=prev:
                    self.move_unit(start_coordinates, previous_square_coordinates, movement_cost)
                self.melee_combat(prev, end)
            else:
                self.move_unit(start_coordinates, end_coordinates, movement_cost)
        else:
            self.ranged_combat(start, end)

    def end_turn(self):
        """
        Heals units and refreshes their movement
        Fortifies unit if still has full movement
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

    def perform_action(self, *args):
        if len(args) == 5:
            self.update_state(*args)
        elif len(args) == 1:
            self.end_turn()

    def binary_search(self, sorted_list: list[float], x: float):
        """
        returns the index of first element grater than x
        if there are none, returns the length of the list
        :param sorted_list:
        :param x:
        :return: int
        """
        left, right = 0, len(sorted_list) - 1
        result_index = None
        while left <= right:
            mid = (left + right) // 2
            if sorted_list[mid] > x:
                result_index = mid
                right = mid - 1
            else:
                left = mid + 1
        if result_index is None:
            result_index = len(sorted_list)
        return result_index

    # RL components
    def get_movement(self, start: Square):
        """
        Returns
        indices of the squares where unit can move to
        indices of previous squares, relevant with combats
        movement costs
        :param start:
        :return: list[int], list[int], list[int]
        """

        max_movement = start.unit.movement_left

        movement_list = [0] # how much movement takes to move here
        square_indices = [start.index]
        previous_square_indices = [start.index]

        ind = 0

        while True:
            if movement_list[ind] > max_movement:
                break
            neighbors = self.index_to_neighbors[square_indices[ind]]
            for n in neighbors:
                if n.movement_cost == -1:
                    continue
                if n.unit and n.unit.team == start.unit.team:
                    continue
                movement = n.movement_cost + movement_list[ind]
                if movement > max_movement:
                    # can always move one if has max movement
                    if n.movement_cost != movement or start.unit.movement_left != start.unit.movement_max:
                        continue
                if n.index in square_indices:
                    continue
                i = self.binary_search(movement_list, movement)
                square_indices.insert(i, n.index)
                movement_list.insert(i, movement)
                previous_square_indices.insert(i, square_indices[ind])
            ind += 1
            if len(movement_list) == ind:
                break
        return square_indices, previous_square_indices, movement_list

    def get_ranged_attacks(self, square: Square):
        enemies = []
        # Range 1
        for neigh in self.coordinates_to_neighbor[square.loc]:
            if neigh.unit and neigh.unit.team != square.unit.team:
                enemies.append(neigh.loc)
        # Range 2
        elevation = 1 if square.terrain in [2, 3] else 0
        for key, value in obstacles.items():
            # key = target, value = obstacles
            for o in value:
                try:  # not sure how of good an idea try-except structure is
                    target = self.coordinates_to_square[key[0]+square.x, key[1]+square.y]
                    if target.unit is not None:
                        if terrain_elevation[self.coordinates_to_square[(square.x+o[0], square.y+o[1])].terrain] <= elevation:
                            enemies.append((target.x, target.y))
                            continue
                except KeyError:
                    pass
        return enemies

    def get_action_space(self):
        actions = []
        for i, unit in enumerate(self.get_team(self.turns.to_play)):
            # melee / movement
            loc = self.coordinates_to_square[unit.location]
            endpoints, previous, cost = self.get_movement(loc)
            for j in range(len(endpoints)):
                start = unit.location
                end = self.squares[endpoints[j]].loc
                prev = self.squares[previous[j]].loc
                costs = cost[j]
                actions.append([start, end, prev, costs, True])
            # ranged
            if unit.ranged_strength != 0 and unit.movement_left > 0:
                targets = self.get_ranged_attacks(self.coordinates_to_square[unit.location])
                for target in targets:
                    actions.append([unit.location, target, unit.location, unit.movement_left, False])

        return actions

    def get_game_state(self):
        pass

    def get_reward(self):
        pass



game = Game(2, 3)
team1 = ["archer", "warrior", "warrior"]
team2 = ["swordsman", "swordsman"]
game.set_units_on_board(team1, team2)


"""
note to self
the communication between logic and AI:
possible actions is called
    actions are stored in format (start, end, previous, movement_cost, move=Bool)
    actually all of the should probably be passed to AI

"""
