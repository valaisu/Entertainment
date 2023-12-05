The goal is to create rules to play a bit of Civilization
More specifically, this program aims to be a small-scale 
battle simulator for 2+ units.

Roadmap:

VERSION 0: bare minimum

The terrain has some variations. Units can be 
moved, and they can engage in combat. 

Create the board from hexagons CHECK
1. draw the hexagons CHECK
2. add hills, rivers, forests CHECK

Create the units 
1. unit movement CHECK
2. display unit stats CHECK
3. unit attack CHECK
4. turns CHECK

VERSION 1: resembles civ6 combat experience

Units:
1. add more units, maybe own file CHECK
2. display fortifying CHECK

Combat:
1. Take the terrain in to account CHECK

Terrain: 
1. generate mountains, lakes, forest+hills CHECK

Movement:
1. Improve the search algorithm CHECK
2. display possible movement when unit is selected CHECK

<--- CURRENTLY HERE

Turns: 
1. Only one team can play at time

    
Missing non-essential features
1. zone control
2. swap units
3. rivers
4. water movement

Advanced features (VERSIONS 4+)
1. map editor
2. train an AI (RL)

AI prerequisites:
1. Get game state
2. Get possible actions
3. Evaluation/reward function
4. Display results

VERSION 2: separation of GUI, game logic and animations
consider using c++ for the processing of the game state

VERSION 3: improve graphics
1. animations
   1. move
   2. combat
   3. end turn

At this point the software kinda has everything it needs,
but the architecture will not be efficient for training AI



VERSION 4: AI Training


