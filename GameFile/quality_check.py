import numpy as np
import random

from cell_handling import CellHandling
from entity import Entity
from game_map import GameMap
import tile_types

#Object which deals with checking quality of dungeon
#This also has a method to put in items
class QualityCheck(CellHandling):
    def __init__(self, dungeon: GameMap) -> None:
        super().__init__(dungeon)
    
    #Public
    def do_floodfill(self, player: Entity, proximity_count: int) -> None:
        color_map = self.__create_color_map()
        pos = self.__pick_position(player, proximity_count)
        new_color_map = self.__floodfill(color_map, pos[0], pos[1])
        self.__place_wall(new_color_map)
        
    #Public
    def quality_check(self, chance_to_live: float) -> bool:
        #Count the floor tile within entire dungeon
        floor_tiles = 0
        for y in range(0, self._dungeon.height):
            for x in range(0, self._dungeon.width):
                if self._dungeon.tiles[x][y] == tile_types.floor:
                    floor_tiles += 1
        #Quality check passed if desired ratio of floor in map
        ratio_of_floor = floor_tiles / (self._dungeon.width * self._dungeon.height)
        passed_check = True
        if ratio_of_floor < (chance_to_live - 0.15):
            passed_check = False
        
        print(floor_tiles)
        print(ratio_of_floor)
        print(passed_check)
        
        return passed_check
    
    #Public
    def place_items(self, tile_proximity: int, probability: float, object_type: str) -> None:
        #Loops through entire game map, checking if position is
        #Suitable to place items, then randomly decide whether to put them in or not
        for y in range(0, self._dungeon.height):
            for x in range(0, self._dungeon.width):
                if self._dungeon.tiles[x][y] == tile_types.floor:
                    if self._alive_neighbour(self._dungeon, x, y) >= tile_proximity and random.random() <= probability:
                        if object_type == "TREASURE":
                            self._dungeon.tiles[x][y] = tile_types.treasure
                        elif object_type == "POTION":
                            self._dungeon.tiles[x][y] = tile_types.potion
                        elif object_type == "EQUIPMENT":
                            self._dungeon.tiles[x][y] = tile_types.equipment
                            
    #Private
    def __create_color_map(self) -> np.array:
        #0 is wall, 1 is floor and 2 is filled floor
        #Create a "color map" to do the flood fill on
        #Color map is based on the dungeon's tiles
        color_map = np.zeros((self._dungeon.width, self._dungeon.height))
        for y in range(0, self._dungeon.height):
            for x in range(0, self._dungeon.width):
                if self._dungeon.tiles[x][y] == tile_types.floor:
                    color_map[x][y] = 1
                    
        return color_map
    
    #Private
    def __pick_position(self, player: Entity, proximity_count: int) -> list[int, int]:
        #Pick a point which is open enough to use as start to flood fill
        #How open is dependent on proximity count
        #Then set the initial position of player character on that position
        suitable = False
        while (not suitable):
            posx = random.randint(0, self._dungeon.width - 1)
            posy = random.randint(0, self._dungeon.height - 1)
            #If tile chosen is a wall, ignore
            if self._dungeon.tiles[posx][posy] == tile_types.wall:
                continue
            #If tile is open enough, choose
            if self._alive_neighbour(self._dungeon, posx, posy) <= proximity_count:
                suitable = True
                
            player.x, player.y = posx, posy

        return [posx, posy]
    
    #Private                
    def __floodfill(self, color_map: list, posx: int, posy: int) -> np.array:
        #Apply floodfill to color_map
        height = self._dungeon.height
        width = self._dungeon.width
        #Use a queue to store tiles which have not been colored
        queue = []
        queue.append([posx, posy])
        while len(queue) > 0:
            #Always do operation on first object in queue each iteration
            n = queue.pop(0)
            if color_map[n[0]][n[1]] == 1:
                #Change color of current tile to 2 (filled floor) if current tile is a floor
                color_map[n[0]][n[1]] = 2
                
                #Check all 4 cardinal direction and see if tile needs to be flooded onto
                if n[0] - 1 >= 0 and color_map[n[0] - 1][n[1]] == 1:
                    queue.append([n[0] - 1, n[1]])

                if n[0] + 1 <= width and color_map[n[0] + 1][n[1]] == 1:
                    queue.append([n[0] + 1, n[1]])
                    
                if n[1] - 1 >= 0 and color_map[n[0]][n[1] - 1] == 1:
                    queue.append([n[0], n[1] - 1])

                if n[1] + 1 <= height and color_map[n[0]][n[1] + 1] == 1:
                    queue.append([n[0], n[1] + 1])
                
        return color_map
    
    #Private
    def __place_wall(self, new_color_map: np.array) -> None:
        #Loop through flooded color map
        #Then fill tiles which are not flooded with walls
        for y in range(0, self._dungeon.height):
            for x in range(0, self._dungeon.width):
                if new_color_map[x][y] != 2:
                    self._dungeon.tiles[x][y] = tile_types.wall