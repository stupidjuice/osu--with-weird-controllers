import pynput as pnp

mouseController = pnp.mouse.Controller()
keyboardController = pnp.keyboard.Controller()

#thanks 6.006 for reminding me these exist lol
movementDict = { "MOUSE_UP": (0, -1), "MOUSE_DOWN": (0, 1), "MOUSE_LEFT": (-1, 0), "MOUSE_RIGHT": (1, 0), "MOUSE_UPLEFT": (-1, 1), "MOUSE_UPRIGHT": (1, 1), "MOUSE_DOWNLEFT": (-1, -1), "MOUSE_DOWNRIGHT": (1, -1) }
clickDict = { "MOUSE_LCLICK" : 0, "KEY_Z": "z", "KEY_X": "x"}

#strength is how far the mouse moves
def mouseMovementEvent(event, strength):
    moveDir = movementDict[event]  
    mouseController.move(moveDir[0] * strength, moveDir[1] * strength)

#i couldnt think of a better name for the "vector" parameter (its just the direction and strength the mouse moves in)
def mouseMovementEventAnalogue(vector):
    pass

def mouseClickEvent(event):
    button = clickDict[event]
    
    if button == 0:
        mouseController.click(pnp.mouse.Button.left)
    else:
        keyboardController.press(button)
        keyboardController.release(button)
        