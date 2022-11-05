import tcod.event

from actions import Action, MovementAction, MapAction

class EventHandler(tcod.event.EventDispatch[Action]):
    def ev_quit(self, event: tcod.event.Quit):
        raise SystemExit()
    
    def ev_keydown(self, event: tcod.event.KeyDown):
        #Store the subclass of Action to variable action. If no
        #valid keys was found, keep it as None
        action = None
        
        #Get key input
        key = event.sym
        
        #Event for arrow keys and "esc"
        if key == tcod.event.K_UP or key == tcod.event.K_w:
            action = MovementAction(dx = 0, dy = -1)
        elif key == tcod.event.K_DOWN or key == tcod.event.K_s:
            action = MovementAction(dx = 0, dy = 1)
        elif key == tcod.event.K_LEFT or key == tcod.event.K_a:
            action = MovementAction(dx = -1, dy = 0)
        elif key == tcod.event.K_RIGHT or key == tcod.event.K_d:
            action = MovementAction(dx = 1, dy = 0)
        
        elif key == tcod.event.K_ESCAPE:
            action = MapAction(-1)
        elif key == tcod.event.K_1:
            action = MapAction(1)
        elif key == tcod.event.K_2:
            action = MapAction(2)
        elif key == tcod.event.K_3:
            action = MapAction(3)
        elif key == tcod.event.K_4:
            action = MapAction(4)
        elif key == tcod.event.K_5:
            action = MapAction(5)
        elif key == tcod.event.K_6:
            action = MapAction(6)
            
        #No valid key pressed
        return action
        