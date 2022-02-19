import tcod

from engine import Engine
from entity import Entity
from input_handler import EventHandler
from procgen import generate_dungeon_bsp

def main() -> None:
    #Set screen dimensions
    screen_width = 80
    screen_height = 50
    
    map_width = 80
    map_height = 45
    
    room_min_dimension = 5
    
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
    
    #Create event handler
    event_handler = EventHandler()
    
    #Initiate entities
    player = Entity(int(screen_width / 2), int(screen_height / 2), "@", WHITE)
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), "@", GREEN)
    entities = {npc, player}
    
    game_map = generate_dungeon_bsp(room_min_dimension=room_min_dimension,
                                    map_width=map_width,
                                    map_height=map_height,
                                    player=player)
    engine = Engine(entities= entities, event_handler= event_handler, game_map= game_map , player= player)
    
    #Create the terminal (screen)
    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset = tileset,
        title = "Yet Another Roguelike Tutorial",
        vsync = True,
        
    ) as context:
        #Create the console (canvas) where everything is drawn onto
        root_console = tcod.Console(screen_width, screen_height, order = "F")
        
        #Main game loop
        while True:
            #Draw and update
            engine.render(console= root_console, context= context)
            
            #Events
            events = tcod.event.wait()
            engine.handle_events(events)
                
if __name__ == "__main__":
    main()