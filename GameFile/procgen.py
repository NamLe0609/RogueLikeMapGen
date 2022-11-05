import numpy as np
from entity import Entity
from bsp import Node
from cellular_automata import CellularAutomata
from quality_check import QualityCheck
import tile_types

from game_map import GameMap

def generate_dungeon_bsp(
    dungeon: GameMap,
    room_min_dimension: int,
    map_width: int, 
    map_height: int,
    player: Entity,
    standalone: bool
    ) -> GameMap:
    """Generate a new dungeon map using bsp."""
    
    """Standalone true for BSP with rooms, false for only corridors. Use size 12 for dungeon"""
    
    if dungeon == None:
        dungeon = GameMap(map_width, map_height)
        
    root_node = Node(0, 0, map_width, map_height, room_min_dimension)    
    root_node.create_subnode()
    root_node.create_room(dungeon,standalone)
    root_node.place_character(player)
    while (dungeon.tiles[player.x][player.y] == tile_types.wall):
        root_node.place_character(player)
    
    quality_check = QualityCheck(dungeon)
    
    quality_check.place_items(3, 0.02, "TREASURE")
    quality_check.place_items(1, 0.01, "EQUIPMENT")
    quality_check.place_items(0, 0.01, "POTION")
    
    return dungeon

def generate_dungeon_cellular(
    ratio_of_floor: float,
    normal_iterations: int,
    indepth_iterations: int,
    map_width: int, 
    map_height: int,
    player: Entity
    ) -> GameMap:
    """Generate a new dungeon map using cellular automata."""
    
    """Generate a noise map, then apply cellular automata indepth algorithm to
    said noise map for a chosen number of iterations. Then, apply normal cellular automata
    algorithm for a chosen number of iterations. Afterwards, do floodfill and check for quality.
    If quality is not met, repeat all again until quality is met"""

    """
    (0.55, 4, 2) for cave
    (0.60, 5, 0) for catacombs
    """
    
    dungeon = GameMap(map_width, map_height)
        
    cellular_automata = CellularAutomata(ratio_of_floor, dungeon)
    quality_check = QualityCheck(dungeon)
    
    good = False
    while (good == False):
        cellular_automata.create_noise_map()
        cellular_automata.cellular_automata_indepth(indepth_iterations)
        cellular_automata.cellular_automata(normal_iterations)
        quality_check.do_floodfill(player, 2)
        good = quality_check.quality_check(ratio_of_floor)
        
    quality_check.place_items(3, 0.02, "TREASURE")
    quality_check.place_items(1, 0.01, "EQUIPMENT")
    quality_check.place_items(0, 0.01, "POTION")
    
    return dungeon
    
def generate_hybrid_ca_bsp(
    ratio_of_floor: float,
    normal_iterations: int,
    indepth_iterations: int,
    room_min_dimension: int,
    map_width: int, 
    map_height: int,
    player: Entity
    ) -> GameMap:
    """Generate a new dungeon map using cellular automata with bsp corridors applied on top"""

    """
    Room Dimension 8-12 layered on top of catacombs (0.60, 5, 0) for best result
    """

    good = False
    while (good == False):
        game_map1 = generate_dungeon_cellular(
            ratio_of_floor = ratio_of_floor,
            normal_iterations = normal_iterations,
            indepth_iterations = indepth_iterations,
            map_width = map_width,
            map_height = map_height,
            player = player
        )

        game_map2 = generate_dungeon_bsp(
            room_min_dimension = room_min_dimension,
            map_width = map_width,
            map_height = map_height,
            player = player,
            dungeon = game_map1,
            standalone = False
        )

        quality_check = QualityCheck(game_map2)
        quality_check.do_floodfill(player, 2)
        good = quality_check.quality_check(0.4)
        
    quality_check.place_items(3, 0.02, "TREASURE")
    quality_check.place_items(1, 0.01, "EQUIPMENT")
    quality_check.place_items(0, 0.01, "POTION")
    
    return game_map2

def generate_hybrid_ca_bsp_ca(
    normal_iterations: int,
    indepth_iterations: int,
    room_min_dimension: int,
    map_width: int, 
    map_height: int,
    player: Entity
    ) -> GameMap:
    """Generate a new dungeon map using bsp, then apply cellular automata and then have bsp corridors placed on top"""

    """
    Room Dimension 4-6 with iterations (2, 3) for best result
    """

    good = False
    while (good == False):
        game_map1 = generate_dungeon_bsp(
            room_min_dimension = room_min_dimension,
            map_width = map_width,
            map_height = map_height,
            player = player,
            dungeon = None,
            standalone = True
        )

        cellular_automata = CellularAutomata(0.40, game_map1)
        cellular_automata.cellular_automata_indepth(indepth_iterations)
        cellular_automata.cellular_automata(normal_iterations)
        
        game_map2 = generate_dungeon_bsp(
            room_min_dimension = room_min_dimension,
            map_width = map_width,
            map_height = map_height,
            player = player,
            dungeon = game_map1,
            standalone = False
        )
    
        quality_check = QualityCheck(game_map2)
        quality_check.do_floodfill(player, 2)
        good = quality_check.quality_check(0.40)
        
    quality_check.place_items(3, 0.02, "TREASURE")
    quality_check.place_items(1, 0.01, "EQUIPMENT")
    quality_check.place_items(0, 0.01, "POTION")
    return game_map1

def generate_loading(
    map_width: int,
    map_height: int,
    ) -> GameMap:
    """Generate a new dungeon map manually with the word "LOADING" on it"""
    
    LOADING = [["#"," ", " ", " ", " ", " ", " ", " ", "#","#"," ", " ", " ", " ", " ", " ", " ", "#"," ", " ", " ", " ", " ", " ", "#","#"," ", " ", " ", " ", "#","#","#","#","#"," ", " ", " ", "#"," ", " ", " ", "#"," ", " ", " ", "#","#","#","#","#"],
    ["#"," ", " ", " ", " ", " ", " ", "#"," ", " ", "#"," ", " ", " ", " ", " ", "#","#","#"," ", " ", " ", " ", " ", "#"," ", " ", "#"," ", " ", " ", " ", "#"," ", " ", " ", " ", " ", "#","#"," ", " ", "#"," ", " ", "#"," ", " ", " ", " ", " "],
    ["#"," ", " ", " ", " ", " ", "#"," ", " ", " ", " ", "#"," ", " ", " ", "#"," ", " ", " ", "#"," ", " ", " ", " ", "#"," ", " ", " ", "#"," ", " ", " ", "#"," ", " ", " ", " ", " ", "#"," ", "#"," ", "#"," ", " ", "#"," ", " ", " ", "#","#","#"],
    ["#"," ", " ", " ", " ", " ", " ", "#"," ", " ", "#"," ", " ", " ", "#","#","#","#","#","#","#"," ", " ", " ", "#"," ", " ", "#"," ", " ", " ", " ", "#"," ", " ", " ", " ", " ", "#"," ", " ", "#","#"," ", " ", "#"," ", " ", " ", " ", "#"],
    ["#","#","#","#","#"," ", " ", " ", "#","#"," ", " ", " ", "#"," ", " ", " ", " ", " ", " ", " ", "#"," ", " ", "#","#"," ", " ", " ", " ", "#","#","#","#","#"," ", " ", " ", "#"," ", " ", " ", "#"," ", " ", " ", "#","#","#","#","#"]]    
    
    dungeon = GameMap(width = map_width, height = map_height)
    dungeon.tiles = np.full((map_width, map_height), fill_value = tile_types.floor, order= "F")
    
    for y in range(0, 5):
        for x in range(0, len(LOADING[y])):
            if LOADING[y][x] == "#":
                dungeon.tiles[x + 14][y + 21] = tile_types.wall
                dungeon.visible[x + 14][y + 21] = tile_types.wall

            
    return dungeon