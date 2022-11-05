from game_map import GameMap
import tile_types

#Parent class that contains methods used to deal with
#Cells around a position
class CellHandling:
    def __init__(self, dungeon: GameMap):
        self._dungeon = dungeon
    
    #Protected
    def _alive_neighbour(self, dungeon: GameMap, posx: int, posy: int) -> int:
        surrounding_wall_tiles = 0
        
        #Iterate all 8 surrounding tile
        #Tiles outside map is considered a wall
        #Skip counting middle tile
        for y in range(posy - 1, posy + 2):
            for x in range(posx - 1, posx + 2):
                if (x == posx and y == posy):
                    continue
                elif y < 0 or y >= dungeon.height or x < 0 or x >= dungeon.width:
                    surrounding_wall_tiles += 1
                elif dungeon.tiles[x][y] == tile_types.wall:
                    surrounding_wall_tiles += 1
                    
        return surrounding_wall_tiles
        
    #Protected
    def _alive_distant_neighbour(self, dungeon: GameMap, posx: int, posy: int) -> int:
        surrounding_wall_tiles = 0
        
        #Iterate 16 extended surrounding tile
        #Tiles outside map is considered a wall
        #Skip counting tiles which are directly adjacent and middle tile
        for y in range(posy - 2, posy + 3):
            for x in range(posx - 2, posx + 3):
                outside_bounds = y < 0 or y >= dungeon.height or x < 0 or x >= dungeon.width
                distant_neighbour = y < posy - 1 or y >= posy + 2 or x < posx - 1 or x >= posx + 2
                if outside_bounds:
                    if distant_neighbour:
                        surrounding_wall_tiles += 1
                else:
                    if distant_neighbour:
                        if dungeon.tiles[x][y] == tile_types.wall:
                            surrounding_wall_tiles += 1
                    
        return surrounding_wall_tiles