import tcod
from entity import Entity
from bsp_methods import Node

from game_map import GameMap

def generate_dungeon_bsp(
    room_min_dimension: int,
    map_width: int, 
    map_height: int,
    player: Entity
    ) -> GameMap:
    """Generate a new dungeon map using bsp."""
    
    """Recursively splits map down either vertically or horizontally
    until cannot split more as byproduct rooms would be smaller than min room size.
    Then, start placing rooms of random sizes within those leaves and connect
    all those rooms toghether."""
        
    dungeon = GameMap(map_width, map_height)
    
    root_node = Node(0, 0, map_width, map_height)    
    root_node.create_subnode(room_min_dimension)
    root_node.create_room(dungeon)
    
    return dungeon
    
    
    
        