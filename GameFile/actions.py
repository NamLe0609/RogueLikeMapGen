from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity

#Main class for all actions
class Action:
    def perform(self, engine: Engine, entity: Entity) -> None:
        """Perform this action with the objects needed to determine its scope.

        `engine` is the scope this action is being performed in.

        `entity` is the object performing the action.

        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()

#Class to deal with when "esc" or number buttons are hit
class MapAction(Action):
    def __init__(self, map_type: int) -> None:
        super().__init__()
        
        self.map_type = map_type
    
    def perform(self, engine: Engine, entity: Entity) -> None:
        if engine.map_type == -1 and self.map_type == -1:
            self.map_type = 0
        engine.map_type = self.map_type

#Class to deal with movements
class MovementAction(Action):
    def __init__(self, dx: int, dy: int):
        super().__init__()
        
        self.dx = dx
        self.dy = dy
        
    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy
        
        if not engine.game_map.in_bounds(dest_x, dest_y):
            return # Destination is out of bounds
        
        if not engine.game_map.tiles["walkable"][dest_x, dest_y]:
            return # Destination is blocked by a tile
        
        entity.move(self.dx, self.dy)