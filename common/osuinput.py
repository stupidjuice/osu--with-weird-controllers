import pynput as pnp

mouseController = pnp.mouse.Controller()
keyboardController = pnp.keyboard.Controller()

#thanks 6.006 for reminding me these exist lol
movementDict = { "MOUSE_UP": (0, -1), "MOUSE_DOWN": (0, 1), "MOUSE_LEFT": (-1, 0), "MOUSE_RIGHT": (1, 0), "MOUSE_UPLEFT": (-1, 1), "MOUSE_UPRIGHT": (1, 1), "MOUSE_DOWNLEFT": (-1, -1), "MOUSE_DOWNRIGHT": (1, -1) }
clickDict = { "MOUSE_LCLICK" : 0, "KEY_Z": "z", "KEY_X": "x"}

currentHeld = { "MOUSE_LCLICK" : False, "KEY_Z": False, "KEY_X": False}

#strength is how far the mouse moves
def mouseMovementEvent(event, strength):
    moveDir = movementDict[event]
    mouseController.move(moveDir[0] * strength, moveDir[1] * strength)

#i couldnt think of a better name for the "vector" parameter (its just the direction and strength the mouse moves in)
def mouseMovementEventAnalogue(vector):
    pass

def mouseClickEvent(event):
    currentHeld[event] = True

def mouseReleaseEvent(event):
    currentHeld[event] = False

def spamClicks():
    for i in currentHeld:
        button = clickDict[i]
        if button == 0:
            mouseController.click(pnp.mouse.Button.left)
        else:
            keyboardController.press(button)