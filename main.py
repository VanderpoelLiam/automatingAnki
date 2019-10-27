#! python3

# german.py - Assists creation of german anki card using word from the command
# line or clipboard

import sys
from re import search
from pyperclip import paste
from webscraping import getSoup, getIpa, getWordClass, getWordForms, isVerb, isNoun
from ankiInteractions import pasteFront, pasteDefinition, pasteBack, \
    pasteFullSentence, pasteExtraInfo, pasteAdd2Cards, clickAdd
from browser import getDriver, loadWordReference, getImage, getTranslation, \
    getTranslation, getSentence, getDefinition
from listener import listenForChoice, listenForNext, listenForCopy, getChoice, listenForClick

# Website URLs
WIKITIONARY = 'https://de.wiktionary.org/wiki/'
LINGUEE = 'https://www.linguee.de/deutsch-englisch/search?source=auto&query='
FREE_DICT = 'https://de.thefreedictionary.com/'

def queryYesNo(question, default="y"):
    valid = {"y": True, "n": False}
    prompt = " [y/n]\n"
    sys.stdout.write(question + prompt)
    listenForChoice()
    return valid[getChoice()]

def clearScreen():
    print("\033[H\033[J")

def getWord():
    if len(sys.argv) > 1:
        # Get word from command line.
        word = sys.argv[1]
    else:
        # Get word from clipboard.
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

    loadWordReference(driver, word)

    make2Cards = queryYesNo("Make 2 cards?")
    if (make2Cards):
        pasteAdd2Cards()

    wiktionarySoup = getSoup(wikitionarySite)
    extraInfo = ""
    wordClass = getWordClass(wiktionarySoup)

    if isVerb(wordClass) or isNoun(wordClass):
        extraInfo = getWordForms(wiktionarySoup, wordClass)

    extraInfo += getIpa(wiktionarySoup)
    pasteExtraInfo(extraInfo)

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

    # needDefintion = queryYesNo("Do I need a definition?")
    # if (needDefintion):
    definition = getDefinition(driver, definitionSites)
    pasteDefinition(definition)
    pasteFront(blankedOutSentence)
    # if (needDefintion):
    getTranslation(driver, definition)

    if isNoun(wordClass):
        print("Remove any gender indicators from example sentence.\n")
        listenForNext()

    getImage(driver, sentence)
    listenForClick()
    clickAdd()

if __name__ == '__main__':
    try:
        driver = getDriver()
        word = getWord()
        main(word, driver)
        clearScreen()
    finally:
        driver.quit()
