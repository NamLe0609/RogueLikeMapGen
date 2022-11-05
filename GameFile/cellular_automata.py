import copy
import random

from cell_handling import CellHandling
import tile_types
from game_map import GameMap

#Object that deals with cellular automata
class CellularAutomata(CellHandling):
    def __init__(self, chance_to_die: float, dungeon: GameMap):
        super().__init__(dungeon)
        self.__chance_to_die = chance_to_die 
    
    #Public
    def create_noise_map(self) -> None:
        #Creates a noise map to start the cellular automata step
        for y in range(1, self._dungeon.height - 1):
            for x in range(1, self._dungeon.width - 1):
                if (random.randint(0, 100) / 100) < self.__chance_to_die:
                    #Get a random number
                    #If number is less than chance to live
                    #Change it into a floor tile
                    self._dungeon.tiles[x][y] = tile_types.floor
                    
    #Public
    def cellular_automata(self, iterations: int) -> None:
        #Applies normal cellular automata for
        #a given amount of iterations
        for i in range(0, iterations):
            self.__cellular_automata_step()
        
    #Public
    def cellular_automata_indepth(self, iterations: int) -> None:
        #Applies indepth cellular automata for
        #a given amount of iterations
        for i in range(0, iterations):
            self.__cellular_automata_step_indepth()
            
    #Private        
    def __cellular_automata_step(self) -> None:
        #Applies normal cellular automata which
        #Only checks for direct neighbour tiles
        old_map = copy.deepcopy(self._dungeon)
        for y in range(0, self._dungeon.height):
            for x in range(0, self._dungeon.width):
                adjacent_wall = self._alive_neighbour(old_map, x, y)
                if self._dungeon.tiles[x][y] == tile_types.wall:
                    if (adjacent_wall >= 4):
                        self._dungeon.tiles[x][y] = tile_types.wall
                    else:
                        self._dungeon.tiles[x][y] = tile_types.floor
                else:
                    if (adjacent_wall >= 5):
                        self._dungeon.tiles[x][y] = tile_types.wall
                    else:
                        self._dungeon.tiles[x][y] = tile_types.floor
                    
    #Private
    def __cellular_automata_step_indepth(self) -> None:
        #Applies indepth cellular automata which
        #Checks for direct and distant (1 tile further) neighbour tiles
        old_map = copy.deepcopy(self._dungeon)
        for y in range(0, self._dungeon.height):
            for x in range(0, self._dungeon.width):
                adjacent_wall = self._alive_neighbour(old_map, x, y)
                distant_adjacent_wall = self._alive_distant_neighbour(old_map, x, y)
                if self._dungeon.tiles[x][y] == tile_types.wall:
                    if (adjacent_wall >= 4):
                        self._dungeon.tiles[x][y] = tile_types.wall
                    else:
                        self._dungeon.tiles[x][y] = tile_types.floor
                else:
                    if (adjacent_wall >= 5 or distant_adjacent_wall <= 2):
                        self._dungeon.tiles[x][y] = tile_types.wall
                    else:
                        self._dungeon.tiles[x][y] = tile_types.floor
