import uuid
import sys
from re import search
from webscraping import WikitionaryParser
from listener import listenForCopy
from pyperclip import paste
from ankiAPI import addNote, storeMediaFile
from browser import getDriver, loadWordReference, getImage, getTranslation, \
    getSentence, getDefinition


class Note(object):
    """Represents an Anki Note."""
    WIKITIONARY = 'https://de.wiktionary.org/wiki/'
    LINGUEE = 'https://www.linguee.de/deutsch-englisch/search?source=auto&query='

    def __init__(self, deck, word):
        super(Note, self).__init__()
        self.deck = deck
        self.word = word
        self.wikitionarySite = self.WIKITIONARY + word
        self.lingueeSite = self.LINGUEE + word

    def setSentence(self, driver):
        sentenceSites = [self.wikitionarySite, self.lingueeSite]
        self.sentence = getSentence(driver, sentenceSites)

    def _wordInSentence(self):
        searchResults = search(self.word + "(?!\w)", self.sentence)
        return(searchResults is not None)

    def setBack(self):
        if self._wordInSentence():
            self.back = self.word
        else:
            print("Copy word to blank out.")
            listenForCopy()
            self.back = paste()

    def _blankOutBack(self):
        return(self.sentence.replace(self.back, "___"))

    def _setBlankedOutSentence(self):
        # TODO - remove gender indicators from sentence if word is a noun
        self.blankedOutSentence = self._blankOutBack()

    def _setExtraInfo(self):
        wikiParser = WikitionaryParser(self.word)
        self.extraInfo = wikiParser.getWordForms() + wikiParser.getIpa()

    def setDefinition(self, driver):
        self.definition = getDefinition(driver, [self.wikitionarySite])

    def setImage(self, driver):
        getImage(driver, self.sentence)
        # TODO - move listener into getImage once this becomes main.py
        listenForCopy()
        # TODO - getting the url is very annoying
        url = paste()
        filename = str(uuid.uuid4()) + ".png"
        storeMediaFile(filename, url)
        self.picture = '<div><img src="' + filename + '"></div>'

    def _setFields(self):
        self._setBlankedOutSentence()
        self._setExtraInfo()
        self.fields = {
            "Front (Example with word blanked out or missing)": self.blankedOutSentence,
            "Front (Picture)": self.picture,
            "Front (Definitions, base word, etc.)": self.definition,
            "Back (a single word/phrase, no context)": self.back,
            "The full sentence (no words blanked out)": self.sentence,
            "Extra Info (Pronunciation, personal connections, conjugations, etc)": self.extraInfo,
            'Make 2 cards? ("y" = yes, blank = no)': "y"
        }

    def uploadNote(self):
        self._setFields()
        addNote(self.deck, self.fields)

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
