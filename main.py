#! python3

# main.py - Assists creation of german anki card using word from the command
# line or clipboard

import sys
from pyperclip import paste
from browser import getDriver, loadWordReference, getTranslation
from note import Note


def getWord():
    if len(sys.argv) > 1:
        word = sys.argv[1]
    else:
        word = paste()
    return(word)

def main(word, driver):
    note = Note("Generated Deck", word)

    loadWordReference(driver, word)

    note.setSentence(driver)
    note.setBack()
    getTranslation(driver, note.sentence)

    note.setDefinition(driver)
    getTranslation(driver, note.definition)

    note.setImage(driver)
    note.uploadNote()


if __name__ == '__main__':
    try:
        driver = getDriver()
        word = getWord()
        main(word, driver)
    finally:
        driver.quit()
