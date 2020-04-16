#! python3

# german.py - Assists creation of german anki card using word from the command
# line or clipboard

import sys
from re import search
from pyperclip import paste
from webscraping import WikitionaryParser
from ankiInteractions import pasteFront, pasteDefinition, pasteBack, \
    pasteFullSentence, pasteExtraInfo, pasteAdd2Cards, clickAdd
from browser import getDriver, loadWordReference, getImage, getTranslation, \
    getSentence, getDefinition
from listener import listenForNext, listenForCopy, listenForClick

# Website URLs
WIKITIONARY = 'https://de.wiktionary.org/wiki/'
LINGUEE = 'https://www.linguee.de/deutsch-englisch/search?source=auto&query='
FREE_DICT = 'https://de.thefreedictionary.com/'

def getWord():
    if len(sys.argv) > 1:
        word = sys.argv[1]
    else:
        word = paste()
    return(word)

def blankOutWord(word, sentence):
    return(sentence.replace(word, "___"))

def wordInSentence(word, sentence):
    searchResults = search(word + "(?!\w)", sentence)
    return(searchResults is not None)

def main(word, driver):
    wikitionarySite = WIKITIONARY + word
    lingueeSite     = LINGUEE + word
    theFreeDictSite = FREE_DICT + word
    sentenceSites = [wikitionarySite, lingueeSite, theFreeDictSite]
    definitionSites = [wikitionarySite, theFreeDictSite]

    pasteAdd2Cards()

    wikiParser = WikitionaryParser(word)
    extraInfo = wikiParser.getWordForms() + wikiParser.getIpa()
    pasteExtraInfo(extraInfo)

    loadWordReference(driver, word)

    sentence = getSentence(driver, sentenceSites)
    if wordInSentence(word, sentence):
        backContent = word
    else:
        print("Copy word to blank out.")
        listenForCopy()
        backContent = paste()

    blankedOutSentence = blankOutWord(backContent, sentence)

    pasteFullSentence(sentence)
    pasteBack(backContent)
    getTranslation(driver, sentence)

    definition = getDefinition(driver, definitionSites)
    pasteDefinition(definition)
    pasteFront(blankedOutSentence)
    getTranslation(driver, definition)

    if isNoun(wordClass):
        print("Remove any gender indicators from example sentence.\n")
        listenForNext()

    getImage(driver, sentence)
    listenForClick()
    clickAdd()


if __name__ == '__main__':
    if len(sys.argv) - 1 > 0:
        repeat = True
    else:
        repeat = False

    try:
        driver = getDriver()
        word = getWord()
        main(word, driver)
        while repeat:
            listenForNext()
            word = paste()
            main(word, driver)
    finally:
        driver.quit()
