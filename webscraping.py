#! python3

# webscraping.py - Handles acessing the internet and processing the html

import requests
import bs4

def getSoup(site):
    response = requests.get(site)
    soup = bs4.BeautifulSoup(response.text, features="html.parser")
    return(soup)

########################################################
############## Wikitionary parsing #####################
########################################################

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

########################################################
################ German.net parsing ####################
########################################################

def getExerciseBox(soup):
    exerciseBox = soup.find("div", {"class": "exercisebox"})
    for linebreak in exerciseBox.find_all('br'):
        linebreak.extract()
    return(exerciseBox)

def parseExerciseSoln(children, index):
    part1 = children[index].split(")")[1].strip()
    blank1 = children[index + 1].text.split(":")[1].split(")")[0].strip()
    part2 = children[index + 2].strip()
    blank2 = children[index + 3].text.split(":")[1].split(")")[0].strip()
    part3 = children[index + 4].strip()
    adjectives = children[index + 9]
    blankSentence = part1 + " ___ " + part2 + " ___ " + part3
    fullSentence = part1 + " " + blank1 + " " + part2 + " " + blank2 + " " + part3
    conjAdj = blank1 + ", " + blank2
    return(blankSentence, fullSentence, conjAdj)

def parseExercise(children, index):
    baseAdj = children[index + 9].text
    return baseAdj

def getParsedExercises(baseOffset, numExercises, exerciseSoup, solutionSoup):
    exerciseChildren = list(getExerciseBox(exerciseSoup).children)
    solutionChildren = list(getExerciseBox(solutionSoup).children)

    blankSentences = []
    fullSentences = []
    conjAdjectives = []
    baseAdjectives = []

    for i in range(numExercises):
        index = 6*i + baseOffset
        blankSentence, fullSentence, conjAdj = parseExerciseSoln(solutionChildren, index)
        blankSentences.append(blankSentence)
        fullSentences.append(fullSentence)
        conjAdjectives.append(conjAdj)

        index = 10*i + baseOffset
        baseAdj = parseExercise(exerciseChildren, index)
        baseAdjectives.append(baseAdj)


    exercises = {
        "frontBlanked": blankSentences,
        "frontDefn": baseAdjectives,
        "back": conjAdjectives,
        "fullSentence": fullSentences
                }

    return(exercises)
