import numpy as np

from tcod.console import Console
import tile_types

class GameMap:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.tiles = np.full((width, height), fill_value = tile_types.wall, order= "F")
        self.visible = np.full((width, height), fill_value = False, order = "F")
        self.explored = np.full((width, height), fill_value = False, order = "F")
        
    def in_bounds(self, x: int, y: int) -> bool:
        #Returns true if both x and y are inside the map boundaries
        return 0 <= x < self.width and 0 <= y < self.height
    
    def fill_border(self) -> None:
        for x in range(0, self.width):
            self.tiles[x][0] = tile_types.wall
            self.tiles[x][self.height - 1] = tile_types.wall
            
        for y in range(0, self.height):
            self.tiles[0][y] = tile_types.wall
            self.tiles[self.width - 1][y] = tile_types.wall
    
    def render(self, console: Console, type: int) -> None:
        """
        Renders the map.

        If a tile is in the "visible" array, then draw it with the "light" colors.
        If it isn't, but it's in the "explored" array, then draw it with the "dark" colors.
        Otherwise, the default is "SHROUD".
        """
        #Render without fog
        if type == -1:
            console.tiles_rgb[0:self.width, 0:self.height] = self.tiles["light"]
        else:
            #Render with fog
            console.tiles_rgb[0: self.width, 0: self.height] = np.select(
                condlist = [self.visible, self.explored],
                choicelist = [self.tiles["light"], self.tiles["dark"]],
                default = tile_types.SHROUD
            )

