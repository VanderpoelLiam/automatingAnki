#! python3

# browser.py - Handles running a selenium browser

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from listener import listenForCopyAndNext, listenForNext

WORD_REFERENCE = 'https://www.wordreference.com/deen/'

def setBrowserLocation(driver):
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

def getImage(driver, sentence):
    imagesSite = 'https://www.google.com/search?q=' + sentence + '&sout=1&hl=en&tbm=isch&oq=v&gs_l=img.3..35i39l2j0l8.4861.6646.0.7238.1.1.0.0.0.0.90.90.1.1.0....0...1ac.1.34.img..0.1.90.SKWUGDKJMsg'
    driver.get(imagesSite)

def getTranslation(sentence):
    googleTranslateSite = GOOGLE_TRANSLATE + sentence
    driver.get(googleTranslateSite)
    print("Read translation, press 'enter' to continue.\n")
    listenForNext()

def getSentence(driver, sites):
    object = "an example sentence"
    sentence = copyFromSite(driver, sites, object)
    return(sentence)

def getDefinition(driver, sites):
    object = "a definition"
    definition = copyFromSite(driver, sites, object)
    return(definition)

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
