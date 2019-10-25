#! python3

# exercises.py - Create anki flashcards based on exercises on german.net
import time
from webscraping import getSoup, getExerciseBox, getParsedExercises
from ankiInteractions import pasteFront, pasteDefinition, pasteBack, \
    pasteFullSentence, clickAdd
from browser import getDriver, getImage
from listener import listenForNext, listenForClick

WEBSITE = "https://german.net/exercises/adjectives/superlative/"

def createExercises(driver, exercises):
    iter = zip(exercises["fullSentence"], exercises["frontBlanked"], \
        exercises["answer"], exercises["hint"])
    for fullSentence, blankedSentence, answer, hint in iter:
        pasteFullSentence(fullSentence)
        pasteBack(answer)
        pasteDefinition("Superlativ: " + hint)
        getImage(driver, fullSentence)
        listenForClick()
        listenForNext()
        pasteFront(blankedSentence)
        time.sleep(0.5)
        clickAdd()

def main():
    # TODO - open website and click check answers button before download html
    # exerciseSoup = getSoup(WEBSITE)

    #############
    import bs4
    f = open("html.txt","r")
    exerciseSoup = bs4.BeautifulSoup(f.read(), features="html.parser")
    f.close()
    f = open("htmlSoln.txt","r")
    solutionSoup = bs4.BeautifulSoup(f.read(), features="html.parser")
    f.close()
    #############
    driver = getDriver()
    exercises = getParsedExercises(exerciseSoup, solutionSoup)
    createExercises(driver, exercises)
    driver.quit()

if __name__ == '__main__':
    main()
