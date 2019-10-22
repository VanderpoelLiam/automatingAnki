#! python3

# browser.py - Handles running a selenium browser

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

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
