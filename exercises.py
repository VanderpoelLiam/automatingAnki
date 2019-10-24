#! python3

# exercises.py - Create anki flashcards based on exercises on german.net
from webscraping import getSoup, getExerciseBox, getParsedExercises
from ankiInteractions import pasteFront, pasteDefinition, pasteBack, \
    pasteFullSentence, clickAdd
from browser import getDriver, getImage
from listener import listenForNext, listenForClick

WEBSITE = "https://german.net/exercises/adjectives/superlative/"

def createExercises(driver, exercises, numberExercises):
    for i in range(numberExercises):
        sentence = exercises["fullSentence"][i]
        pasteFullSentence(sentence)
        pasteBack(exercises["back"][i])
        pasteDefinition("Superlativ: " + exercises["frontDefn"][i])
        getImage(driver, sentence)
        listenForClick()
        listenForNext()
        pasteFront(exercises["frontBlanked"][i])
        clickAdd()

def main():
    # driver = getDriver()
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

    baseOffset = 8
    numberExercises = 11
    exercises = getParsedExercises(baseOffset, numberExercises, exerciseSoup, solutionSoup)
    import pprint as pp
    pp.pprint(exercises)

    # createExercises(driver, exercises, numberExercises)


if __name__ == '__main__':
    main()
    driver.quit()
