#! python3

# listener.py - Listens for keyboard and mouse events
from pynput import mouse
from pynput import keyboard

CTRL_C = {keyboard.Key.ctrl, keyboard.KeyCode.from_char('c')}
KEYS_SEEN = set()
COPY_OCCURED = False
CHOICE = "y"
HORIZONTAL_MIDPOINT = 960

def onChoice(key):
    global CHOICE
    if key == keyboard.Key.enter or key == keyboard.KeyCode.from_char('y'):
        CHOICE = "y"
        return(False)
    elif key == keyboard.KeyCode.from_char('n'):
        CHOICE = "n"
        return(False)

def listenForChoice():
    with keyboard.Listener(on_release=onChoice) as listener:
        listener.join()

def getChoice():
    return CHOICE

def onNext(key):
    if key == keyboard.Key.enter:
        return(False)

def listenForNext():
    with keyboard.Listener(on_release=onNext) as listener:
        listener.join()

def isCopyKey(key):
    global KEYS_SEEN
    if key in CTRL_C:
        KEYS_SEEN.add(key)
        if all(k in KEYS_SEEN for k in CTRL_C):
            KEYS_SEEN = set()
            return(True)
    return(False)

def getCopyOccured():
    global COPY_OCCURED
    return(COPY_OCCURED)

def setCopyOccured(value):
    global COPY_OCCURED
    COPY_OCCURED = value
    return

def onCopy(key):
    if isCopyKey(key):
        return(False)

def listenForCopy():
    with keyboard.Listener(on_release=onCopy) as listener:
        listener.join()

def onCopyOrNext(key):
    if key == keyboard.Key.enter:
        return(False)
    elif isCopyKey(key):
        setCopyOccured(True)
        return(False)

def listenForCopyAndNext():
    with keyboard.Listener(on_release=onCopyOrNext) as listener:
        listener.join()

def onClick(x, y, button, pressed):
    if button == mouse.Button.left:
       if not pressed:
        if x > HORIZONTAL_MIDPOINT:
            return False

def listenForClick():
    with mouse.Listener(on_click=onClick) as listener:
        listener.join()
