import tcod

from engine import Engine
from entity import Entity
from game_map import GameMap
from input_handler import EventHandler
from procgen import *

def main() -> None:
    #Set screen dimensions
    screen_width = 80
    screen_height = 50
    
    map_width = 80
    map_height = 50
    
    #Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    
    #Load in tile sheet
    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )
    
    #Initiate event handler
    event_handler = EventHandler()
    
    #Initiate entities
    player = Entity(int(screen_width / 2), int(screen_height / 2), "@", WHITE)
    entities = {player}
    
    #Initiate map
    game_map = GameMap(width = map_width, height = map_height)
    
    #Initiate engine
    engine = Engine(entities= entities, event_handler= event_handler, game_map= game_map, player= player)
    

    #Create the terminal (screen) on which graphics will be displayed
    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset = tileset,
        title = "Procedural Generation Roguelike",
        vsync = True,
        
    ) as context:
        #Create the console (canvas) where everything is drawn onto
        #To then be displayed on the screen
        root_console = tcod.Console(screen_width, screen_height, order = "F")
        
        #Main game loop
        while True:
            
            #If ESC or 1-5 have been pressed
            #Deals with changing map type
            if (engine.map_type > 0):
                #Display loading screen between each generation
                game_map = generate_loading(map_width, map_height)
                engine.game_map = game_map
                engine.render(console= root_console, context= context)
                    
                if engine.map_type == 1:
                    #Binary space partitioning (CASTLE/RECTANGULAR ROOMS)
                    game_map = generate_dungeon_bsp(
                        dungeon = None,
                        room_min_dimension = 12,
                        map_width = map_width,
                        map_height = map_height,
                        player = player,
                        standalone = True
                    )
                    
                elif engine.map_type == 2:
                    #CELLULAR AUTOMATA (CAVERN)
                    game_map = generate_dungeon_cellular(
                        ratio_of_floor = 0.55,
                        indepth_iterations = 4,
                        normal_iterations = 2,
                        map_width = map_width,
                        map_height = map_height,
                        player = player
                    )
                    
                elif engine.map_type == 3:
                    #CELLULAR AUTOMATA (CATACOMBS)
                    game_map = generate_dungeon_cellular(
                        ratio_of_floor = 0.60,
                        indepth_iterations = 5,
                        normal_iterations = 0,
                        map_width = map_width,
                        map_height = map_height,
                        player = player
                    )
                    
                elif engine.map_type == 4:
                    #HYBRID (OPEN SEWERS)
                    game_map = generate_hybrid_ca_bsp(
                        ratio_of_floor = 0.75,
                        indepth_iterations = 1,
                        normal_iterations = 1,
                        room_min_dimension = 12,
                        map_width=map_width,
                        map_height=map_height,
                        player=player
                    )
                
                elif engine.map_type == 5:
                    #HYBRID (CLOSED SEWERS)
                    game_map = generate_hybrid_ca_bsp_ca(
                        indepth_iterations = 2,
                        normal_iterations = 3,
                        room_min_dimension = 4,
                        map_width=map_width,
                        map_height=map_height,
                        player=player
                    )
                    
                elif engine.map_type == 6:
                    #Binary space partitioning (MAZE)
                    game_map = generate_dungeon_bsp(
                        dungeon = None,
                        room_min_dimension = 3,
                        map_width = map_width,
                        map_height = map_height,
                        player = player,
                        standalone=True
                    )
                
                #Update the game map, reset check for map change input then update fov of player in new map
                engine.game_map = game_map
                engine.map_type = 0
                engine.update_fov()
                
            #Draw onto console (canvas) and update display
            #To show the new canvas
            engine.render(console= root_console, context= context)
            
            #Handle events
            events = tcod.event.wait()
            engine.handle_events(events)
                
#Run program
if __name__ == "__main__":
    main()
    
