#! python3

# note.py - Handles note creation in Anki

import uuid
from re import search
from webscraping import WikitionaryParser
from listener import listenForCopy
from pyperclip import paste
from ankiAPI import addNote, storeMediaFile
from browser import getImage, getSentence, getDefinition
from germanGenderIndicators import NounSentence


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
        self.wikiParser = WikitionaryParser(self.word)

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

    def _blankOutBack(self, sentence):
        return(sentence.replace(self.back, "___"))


    def _setBlankedOutSentence(self):
        if self.wikiParser.isNoun():
            nounSentence = NounSentence(self.back, self.sentence)
            sentenceRemovedGender = nounSentence.removeGenderIndicator()
            self.blankedOutSentence = self._blankOutBack(sentenceRemovedGender)
        else:
            self.blankedOutSentence = self._blankOutBack(self.sentence)

    def _setExtraInfo(self):
        self.extraInfo = self.wikiParser.getWordForms() + self.wikiParser.getIpa()

    def setDefinition(self, driver):
        self.definition = getDefinition(driver, [self.wikitionarySite])

    def setImage(self, driver):
        getImage(driver, self.sentence)
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
