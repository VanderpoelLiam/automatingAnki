
#! python3

# german.py - Assists creation of german anki card using word from the command
# line or clipboard

import pyperclip
import sys
import requests
import bs4
import pyautogui
import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pynput import mouse
from pynput import keyboard
from re import search

WIKITIONARY = 'https://de.wiktionary.org/wiki/'
LINGUEE = 'https://www.linguee.de/deutsch-englisch/search?source=auto&query='
FREE_DICT = 'https://de.thefreedictionary.com/'
WORD_REFERENCE = 'https://www.wordreference.com/deen/'
GOOGLE_TRANSLATE = 'https://translate.google.ca/#view=home&op=translate&sl=de&tl=en&text='

FRONT = (1000, 163)
DEFINITION = (1000, 283)
BACK = (1000, 340)
FULL_SENTENCE = (1000, 401)
EXTRA_INFO = (1000, 460)
GET_2_CARDS = (1000, 522)
ADD = (1695, 1055)
HORIZONTAL_MIDPOINT = 960

VERB = 1
NOUN = 2
OTHER_WORD_CLASS = 3

CTRL_C = {keyboard.Key.ctrl, keyboard.KeyCode.from_char('c')}
KEYS_SEEN = set()
COPY_OCCURED = False
CHOICE = "y"


def queryYesNo(question, default="y"):
    valid = {"y": True, "n": False}
    prompt = " [y/n]\n"
    sys.stdout.write(question + prompt)
    listenForChoice()
    return valid[CHOICE]

def getSoup(site):
    response = requests.get(site)
    soup = bs4.BeautifulSoup(response.text, features="html.parser")
    return(soup)

def getIpa(wiktionarySoup):
    ipa = wiktionarySoup.select('.ipa')[0].text
    return(ipa)

def getWordClassIndicator(wiktionarySoup):
    return(wiktionarySoup.h3.text)

def getWordClass(wiktionarySoup):
    wordClassIndicator = getWordClassIndicator(wiktionarySoup)
    if "Substantiv" in wordClassIndicator:
        return(NOUN)
    elif "Verb" in wordClassIndicator:
        return(VERB)
    else:
        return(OTHER_WORD_CLASS)

def getWorttrennung(wiktionarySoup):
    worttrennung = wiktionarySoup.find(string="Worttrennung:").find_next('dd')
    return(worttrennung.text)

def formatVerb(worttrennung):
    verbForms = worttrennung.split(',')

    infinitif = verbForms[0]
    praeterutum = verbForms[1].split(":")[1].strip()
    partizip = verbForms[2].split(":")[1].strip()

    verbForms = infinitif + '\n' + praeterutum + '\n' + partizip + "\n"
    return(verbForms)

def getGender(wiktionarySoup):
    wordClassIndicator = getWordClassIndicator(wiktionarySoup)
    genderInfo = wordClassIndicator.split(',')[1].strip()
    gender = genderInfo.split('[')[0]
    if gender == "n":
        return("das")
    elif gender == "f":
        return("die")
    elif gender == "m":
        return("der")
    else:
        raise ValueError('Gender is not one of n, f, m.')

def formatNoun(gender, worttrennung):
    nounForms = worttrennung.split(',')
    singular = gender + " " + nounForms[0]

    if nounForms[1].strip() == "kein Plural":
        plural = "kein Plural"
    else:
        plural = nounForms[1].split(":")[1].strip()

    wordForms = singular + '\n' + plural + "\n"
    return(wordForms)

def getWordForms(wiktionarySoup, wordClass):
    worttrennung = getWorttrennung(wiktionarySoup)

    if wordClass == VERB:
        wordForms = formatVerb(worttrennung)
    if wordClass == NOUN:
        gender = getGender(wiktionarySoup)
        wordForms = formatNoun(gender, worttrennung)

    return(wordForms)

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

def setBrowserLocation(driver):
    # Moves window into right spot normal I3
    # pyautogui.hotkey('alt', 'r')
    # pyautogui.press('down')
    # pyautogui.press('down')
    # pyautogui.press('down')
    # pyautogui.press('esc')
    # pyautogui.hotkey('alt', 'up')

    # # Moves window into right spot normal UBUNTU
    driver.set_window_position(0, 0)
    driver.set_window_size(960, 1053)

def getDriver():
    capa = DesiredCapabilities.FIREFOX
    capa["pageLoadStrategy"] = "none"
    driver = webdriver.Firefox(desired_capabilities=capa)
    setBrowserLocation(driver)
    return(driver)

def loadWordReference(driver, word):
    wordReferenceSite = WORD_REFERENCE + word
    wait = WebDriverWait(driver, 5)
    driver.get(wordReferenceSite)
    wait.until(EC.presence_of_element_located((By.ID, 'articleWRD')))
    driver.execute_script("window.stop();")

def clickAndPaste(location, text):
    pyautogui.click(location)
    pyperclip.copy(text)
    pyautogui.hotkey('ctrl', 'v')

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

def onClick(x, y, button, pressed):
    if button == mouse.Button.left:
       if not pressed:
        if x > HORIZONTAL_MIDPOINT:
            pyautogui.moveTo(ADD, duration=1)
            pyautogui.click()
            return False

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
        clickAndPaste(GET_2_CARDS, "y")

    wiktionarySoup = getSoup(wikitionarySite)
    extraInfo = ""
    wordClass = getWordClass(wiktionarySoup)

    if wordClass == VERB or wordClass == NOUN:
        extraInfo = getWordForms(wiktionarySoup, wordClass)

    extraInfo += getIpa(wiktionarySoup)
    clickAndPaste(EXTRA_INFO, extraInfo)

    sentence = getSentence(driver, sentenceSites)
    if wordInSentence(word, sentence):
        backContent = word
    else:
        print("Copy word to blank out.")
        listenForCopy()
        backContent = pyperclip.paste()

    blankedOutSentence = blankOutWord(backContent, sentence)

    clickAndPaste(FULL_SENTENCE, sentence)
    clickAndPaste(BACK, backContent)
    getTranslation(sentence)

    needDefintion = queryYesNo("Do I need a definition?")
    if (needDefintion):
        definition = getDefinition(driver, definitionSites)
        clickAndPaste(DEFINITION, definition)
    clickAndPaste(FRONT, blankedOutSentence)
    if (needDefintion):
        getTranslation(definition)

    if wordClass != VERB:
        print("Remove any gender indicators from example sentence.\n")
        listenForNext()

    getImage(sentence)
    clickAddWhenDropImage()


if __name__ == '__main__':
    # Number seconds to wait between actions
    pyautogui.PAUSE = 0.3
    try:
        driver = getDriver()
        word = getWord()
        main(word, driver)
        clearScreen()
    finally:
        driver.quit()
