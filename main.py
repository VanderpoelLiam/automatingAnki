#! python3

# german.py - Assists creation of german anki card using word from the command
# line or clipboard

import pyperclip
import sys
import time
from pynput import mouse
from pynput import keyboard
from re import search

from webscraping import getSoup, getIpa, getWordClass, getWordForms
from ankiInteractions import pasteFront, pasteDefinition, pasteBack, \
    pasteFullSentence, pasteExtraInfo, pasteAdd2Cards, onClick
from browser import getDriver, loadWordReference

# Website URLs
WIKITIONARY = 'https://de.wiktionary.org/wiki/'
LINGUEE = 'https://www.linguee.de/deutsch-englisch/search?source=auto&query='
FREE_DICT = 'https://de.thefreedictionary.com/'
GOOGLE_TRANSLATE = 'https://translate.google.ca/#view=home&op=translate&sl=de&tl=en&text='

VERB = 1
NOUN = 2
OTHER_WORD_CLASS = 3

CTRL_C = {keyboard.Key.ctrl, keyboard.KeyCode.from_char('c')}
KEYS_SEEN = set()
COPY_OCCURED = False
CHOICE = "y"

# TODO - Continue migration of brower relevant code to browser.py
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

def getTranslation(sentence):
    googleTranslateSite = GOOGLE_TRANSLATE + sentence
    driver.get(googleTranslateSite)
    print("Read translation, press 'enter' to continue.\n")
    listenForNext()

def getImage(sentence):
    imagesSite = 'https://www.google.com/search?q=' + sentence + '&sout=1&hl=en&tbm=isch&oq=v&gs_l=img.3..35i39l2j0l8.4861.6646.0.7238.1.1.0.0.0.0.90.90.1.1.0....0...1ac.1.34.img..0.1.90.SKWUGDKJMsg'
    driver.get(imagesSite)

def getSentence(driver, sites):
    object = "an example sentence"
    sentence = copyFromSite(driver, sites, object)
    return(sentence)

def getDefinition(driver, sites):
    object = "a definition"
    definition = copyFromSite(driver, sites, object)
    return(definition)

def clickAddWhenDropImage():
    with mouse.Listener(on_click=onClick) as listener:
        listener.join()

def wordInSentence(word, sentence):
    searchResults = search(word + "(?!\w)", sentence)
    return(searchResults is not None)

def isCopyKey(key):
    global KEYS_SEEN
    if key in CTRL_C:
        KEYS_SEEN.add(key)
        if all(k in KEYS_SEEN for k in CTRL_C):
            KEYS_SEEN = set()
            return(True)
    return(False)

def onCopyOrNext(key):
    global COPY_OCCURED
    if key == keyboard.Key.enter:
        return(False)
    elif isCopyKey(key):
        COPY_OCCURED = True
        return(False)

def listenForCopyAndNext():
    with keyboard.Listener(on_release=onCopyOrNext) as listener:
        listener.join()

def copyFromSite(driver, sites, object):
    global COPY_OCCURED
    print("Copy ", object)
    print("Or press the 'enter' key for the next site.")
    for site in sites:
        if (not COPY_OCCURED):
            driver.get(site)
            listenForCopyAndNext()
        else:
            break
    COPY_OCCURED = False
    clipboard = pyperclip.paste()
    return(clipboard)

def onCopy(key):
    if isCopyKey(key):
        return(False)

def listenForCopy():
    with keyboard.Listener(on_release=onCopy) as listener:
        listener.join()

def onNext(key):
    if key == keyboard.Key.enter:
        return(False)

def listenForNext():
    with keyboard.Listener(on_release=onNext) as listener:
        listener.join()

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

    getImage(sentence)
    clickAddWhenDropImage()


if __name__ == '__main__':
    try:
        driver = getDriver()
        word = getWord()
        main(word, driver)
        clearScreen()
    finally:
        driver.quit()
