#! python3

# ankiInteractions.py - Handles interactions with Anki interface

import pyautogui
import pyperclip

# Number seconds to wait between actions
pyautogui.PAUSE = 0.3

# Anki interface locations on screen
FRONT = (1000, 163)
DEFINITION = (1000, 283)
BACK = (1000, 340)
FULL_SENTENCE = (1000, 401)
EXTRA_INFO = (1000, 460)
GET_2_CARDS = (1000, 522)

ADD = (1695, 1055)
HORIZONTAL_MIDPOINT = 960

def clickAndPaste(location, text):
    pyautogui.click(location)
    pyperclip.copy(text)
    pyautogui.hotkey('ctrl', 'v')

def pasteFront(text):
    clickAndPaste(FRONT, text)

def pasteDefinition(text):
    clickAndPaste(DEFINITION, text)

def pasteBack(text):
    clickAndPaste(BACK, text)

def pasteFullSentence(text):
    clickAndPaste(FULL_SENTENCE, text)

def pasteExtraInfo(text):
    clickAndPaste(EXTRA_INFO, text)

def pasteAdd2Cards():
    clickAndPaste(GET_2_CARDS, "y")

def onClick(x, y, button, pressed):
    if button == mouse.Button.left:
       if not pressed:
        if x > HORIZONTAL_MIDPOINT:
            pyautogui.moveTo(ADD, duration=1)
            pyautogui.click()
            return False
