#! python3

# main.py - Assists creation of german anki card using word from the command
# line or clipboard

import argparse
from pyperclip import paste
from browser import getDriver, loadWordReference, getTranslation
from note import Note
from listener import listenForCopy


def main(word, driver):
    # note = Note("Generated Deck", word)
    note = Note("German Words and Grammar", word)

    loadWordReference(driver, word)

    note.setSentence(driver)
    note.setBack()
    getTranslation(driver, note.sentence)

    note.setDefinition(driver)
    getTranslation(driver, note.definition)

    note.setImage(driver)
    note.uploadNote()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create German Anki Cards.')
    parser.add_argument('-r',
                        required=False,
                        action='store_true',
                        default=False,
                        help='Repeat the card creation process (t/F).')

    parser.add_argument('--word',
                        default=paste(),
                        help='Create Anki Card with this word.')


    args = parser.parse_args()

    try:
        # TODO: add option to edit card before continue
        # TODO: noun matching should handle capitals
        # TODO: add ability to select two words to blank out for
        #       separable verbs
        driver = getDriver()
        main(args.word, driver)
        while args.r:
            print("Copy the next word.\n")
            listenForCopy()
            main(paste(), driver)
    finally:
        driver.quit()
