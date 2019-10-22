#! python3

# exercises.py - Create anki flashcards based on exercises on german.net
from webscraping import getSoup, getExerciseBox, getParsedExercises
from ankiInteractions import pasteFront, pasteDefinition, pasteBack, \
    pasteFullSentence

WEBSITE = "https://german.net/exercises/adjectives/endings/"

"exercisebox"

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

    baseOffset = 8
    numberExercises = 11
    exercises = getParsedExercises(baseOffset, numberExercises, exerciseSoup, solutionSoup)


    
    for i in range(numberExercises):
        pasteFullSentence(exercises["fullSentence"][i])
        pasteBack(exercises["back"][i])
        pasteDefinition(exercises["frontDefn"][i])

        pasteFront(exercises["frontBlanked"][i])
        break

if __name__ == '__main__':
    main()
