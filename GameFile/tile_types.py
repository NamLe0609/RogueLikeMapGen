from typing import Tuple

import numpy as np

#Create new data type for graphics
graphic_dt = np.dtype(
    [
        ("ch", np.int32),  #Unicode codepoint
        ("fg", "3B"),  #3 unsigned bytes, for RGB colors (foreground)
        ("bg", "3B"),  #3 unsigned bytes, for RGB colors (background)
    ]
)

#Create new data type for tile attribute
tile_dt = np.dtype(
    [
        ("walkable", bool),  #True if this tile can be walked over
        ("transparent", bool), #True if this tile doesn't block FOV
        ("dark", graphic_dt),  #Graphics for when this tile is not in FOV
        ("light", graphic_dt) #Graphics for when tile is in FOV
    ]
)

def new_tile(
    *,
    walkable: bool,
    transparent: bool,
    dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
    light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]]
) -> np.ndarray:
    #Helper function to define tile types
    return np.array((walkable, transparent, dark, light), dtype = tile_dt)

#Array representing tiles which are in fog of war (not explored, not visible)
SHROUD = np.array((ord(" "), (255, 255, 255), (0, 0, 0)), dtype = graphic_dt)

""" floor = new_tile(
    walkable = True, 
    transparent = True,
    dark = (ord(" "), (255, 255, 255), (50, 50, 150)),
    light = (ord(" "), (255, 255, 255), (50, 50, 150))
)

wall = new_tile(
    walkable = False,
    transparent = False,
    dark = (ord(" "), (255, 255, 255), (0, 0, 100)),
    light=(ord(" "), (255, 255, 255), (0, 0, 100))
) """

#Code for more traditional roguelike look
floor = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord("."), (100, 100, 100), (0, 0, 0)),
    light=(ord("."), (200, 200, 200), (0, 0, 0)),
)
wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord("#"), (100, 100, 100), (0, 0, 0)),
    light=(ord("#"), (200, 200, 200), (0, 0, 0)),
)

treasure = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord("T"), (130, 110, 50), (0, 0, 0)),
    light=(ord("T"), (200, 180, 50), (0, 0, 0)),
)

potion = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord("P"), (255, 100, 100), (0, 0, 0)),
    light=(ord("P"), (255, 10, 10), (0, 0, 0)),
)

equipment = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord("E"), (102, 140, 255), (0, 0, 0)),
    light=(ord("E"), (0, 64, 255), (0, 0, 0)),
)

