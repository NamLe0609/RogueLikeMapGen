from typing import Set, Iterable, Any

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from entity import Entity
from game_map import GameMap
from input_handler import EventHandler
from procgen import *

class Engine:
    def __init__(self, entities: Set[Entity], event_handler: EventHandler, game_map: GameMap, player: Entity):
        self.entities = entities
        self.game_map = game_map
        self.player = player
        self.update_fov()
        self.map_type = 0
        self.__event_handler = event_handler
        
    #Public
    def handle_events(self, events: Iterable[Any]) -> None:
            for event in events:

                #Sends event to the corresponding 
                #method that deals with it 
                action = self.__event_handler.dispatch(event)
                
                if action is None:
                    continue
                
                action.perform(self, self.player)
                
                self.update_fov()
                
    #Public
    def update_fov(self) -> None:
        """Compute map based on player's point of view"""
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius = 8
        )
        # If a tile is "visible" it should be added to "explored"
        self.game_map.explored |= self.game_map.visible
                
    #Public
    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console, self.map_type)
        
        #Put every entity on canvas
        for entity in self.entities:
            #Only print entities in FOV
            if self.game_map.visible[entity.x, entity.y]:
                console.print(entity.x, entity.y, entity.char, fg = entity.color)

        #Put everything on canvas to screen
        context.present(console)
        
        console.clear()