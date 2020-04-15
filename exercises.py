#! python3

# exercises.py - Create anki flashcards based on exercises on german.net
import time
from webscraping import getExerciseBox, getParsedExercises, \
    DROPDOWN, BLANK
from ankiInteractions import pasteFront, pasteDefinition, pasteBack, \
    pasteFullSentence, clickAdd
from browser import getDriver, getImage
from listener import listenForNext, listenForClick

WEBSITE = "https://german.net/exercises/prepositions/dative/"

def createExercises(driver, exercises):
    iter = zip(exercises["fullSentence"], exercises["frontBlanked"], \
        exercises["answer"], exercises["hint"])
    i = 0
    for fullSentence, blankedSentence, answer, hint in iter:
        i += 1
        if i > 0:
            pasteFullSentence(fullSentence)
            pasteBack(answer)
            pasteDefinition(hint)
            getImage(driver, fullSentence)
            listenForClick()
            listenForNext()
            pasteFront(blankedSentence)
            time.sleep(0.5)
            clickAdd()

def main():
    f = open("html.txt","r")
    exerciseSoup = bs4.BeautifulSoup(f.read(), features="html.parser")
    f.close()
    f = open("htmlSoln.txt","r")
    solutionSoup = bs4.BeautifulSoup(f.read(), features="html.parser")
    f.close()
    driver = getDriver()
    try:
        exercises = getParsedExercises(exerciseSoup, solutionSoup, DROPDOWN)
        createExercises(driver, exercises)
    finally:
        driver.quit()
        pass

if __name__ == '__main__':
    main()
