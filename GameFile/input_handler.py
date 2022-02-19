import tcod.event

from actions import Action, EscapeAction, MovementAction

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
        if key == tcod.event.K_UP:
            action = MovementAction(dx = 0, dy = -1)
        elif key == tcod.event.K_DOWN:
            action = MovementAction(dx = 0, dy = 1)
        elif key == tcod.event.K_LEFT:
            action = MovementAction(dx = -1, dy = 0)
        elif key == tcod.event.K_RIGHT:
            action = MovementAction(dx = 1, dy = 0)
        
        elif key == tcod.event.K_ESCAPE:
            action = EscapeAction()
            
        #No valid key pressed
        return action
        