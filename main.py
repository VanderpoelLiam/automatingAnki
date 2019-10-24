#! python3

# german.py - Assists creation of german anki card using word from the command
# line or clipboard

import pyperclip
import sys
from re import search
from webscraping import getSoup, getIpa, getWordClass, getWordForms
from ankiInteractions import pasteFront, pasteDefinition, pasteBack, \
    pasteFullSentence, pasteExtraInfo, pasteAdd2Cards
from browser import getDriver, loadWordReference, getImage, getTranslation \
    getTranslation, getSentence, getDefinition
from listener import listenForChoice, listenForNext, listenForCopy, \
    clickAddWhenDropImage

# Website URLs
WIKITIONARY = 'https://de.wiktionary.org/wiki/'
LINGUEE = 'https://www.linguee.de/deutsch-englisch/search?source=auto&query='
FREE_DICT = 'https://de.thefreedictionary.com/'
GOOGLE_TRANSLATE = 'https://translate.google.ca/#view=home&op=translate&sl=de&tl=en&text='

VERB = 1
NOUN = 2
OTHER_WORD_CLASS = 3


def queryYesNo(question, default="y"):
    valid = {"y": True, "n": False}
    prompt = " [y/n]\n"
    sys.stdout.write(question + prompt)
    listenForChoice()
    return valid[CHOICE]

def clearScreen():
    print("\033[H\033[J")

def getWord():
    if len(sys.argv) > 1:
        # Get word from command line.
        word = sys.argv[1]
    else:
        # Get word from clipboard.
        word = pyperclip.paste()
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

    if wordClass == VERB or wordClass == NOUN:
        extraInfo = getWordForms(wiktionarySoup, wordClass)

    extraInfo += getIpa(wiktionarySoup)
    pasteExtraInfo(extraInfo)

    sentence = getSentence(driver, sentenceSites)
    if wordInSentence(word, sentence):
        backContent = word
    else:
        print("Copy word to blank out.")
        listenForCopy()
        backContent = pyperclip.paste()

    blankedOutSentence = blankOutWord(backContent, sentence)

    # TODO what does this next line do?
    # backContent(sentence)
    pasteBack(backContent)
    getTranslation(sentence)

    needDefintion = queryYesNo("Do I need a definition?")
    if (needDefintion):
        definition = getDefinition(driver, definitionSites)
        pasteDefinition(definition)
    pasteFront(blankedOutSentence)
    if (needDefintion):
        getTranslation(definition)

    if wordClass != VERB:
        print("Remove any gender indicators from example sentence.\n")
        listenForNext()

    getImage(driver, sentence)
    clickAddWhenDropImage()

if __name__ == '__main__':
    try:
        driver = getDriver()
        word = getWord()
        main(word, driver)
        clearScreen()
    finally:
        driver.quit()
