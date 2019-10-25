#! python3

# webscraping.py - Handles scraping from websites and processing the html

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
import pprint as pp

def getExerciseBox(soup):
    exerciseBox = soup.find("div", {"class": "exercisebox"})
    # for linebreak in exerciseBox.find_all('br'):
    #     linebreak.extract()
    return(exerciseBox)

def getAnswers(solutionSoup):
    answerSoup = solutionSoup.find_all("span", class_="resultbox2")
    answers = []
    for answer in answerSoup:
        rawText = answer.text
        textAfterColon = rawText.split(":")[1]
        textBeforeParenthesis = textAfterColon.split(")")[0]
        finalText = textBeforeParenthesis.strip()
        answers.append(finalText)
    return(answers)

def getSentenceComponents(soup):
    exerciseBox = getExerciseBox(soup)
    components = []
    for item in exerciseBox.select(".resultbox2"):
        rawText1 = item.previous_sibling
        rawText2 = item.next_sibling
        text1 = rawText1.split(")")[1].strip()
        text2 = rawText2.strip()
        component = [text1, text2]
        components.append(component)
    return(components)

def interleave(list, string):
    return(list[0] + " " +  string + " "  + list[1])

def getFullSentences(sentenceComponents, answers):
    sentences = []
    for component, answer in zip(sentenceComponents, answers):
        sentence = interleave(component, answer)
        sentences.append(sentence)
    return(sentences)

def getSentencesWithBlanks(fullSentences, answers):
    sentences = []
    for sentence, answer in zip(fullSentences, answers):
        blankedSentence = sentence.replace(answer, "___")
        sentences.append(blankedSentence)
    return(sentences)

def getHints(soup):
    hintSoup = soup.find_all("span", class_="hint_text")
    hints = []
    i = 0
    for form in hintSoup:
        text = form.text
        if text is not "":
            if i == 0:
                i = 1
                continue
            hints.append(text)

    return(hints)

def getParsedExercises(exerciseSoup, solutionSoup):
    answers = getAnswers(solutionSoup)
    sentenceComponents = getSentenceComponents(solutionSoup)
    fullSentences = getFullSentences(sentenceComponents, answers)
    blankedSentences = getSentencesWithBlanks(fullSentences, answers)
    hints = getHints(exerciseSoup)

    exercises = {
        "frontBlanked": blankedSentences,
        "frontDefn": hints,
        "back": answers,
        "fullSentence": fullSentences
                }

    assert(len(answers) == len(fullSentences))
    assert(len(answers) == len(blankedSentences))
    assert(len(answers) == len(hints))

    return(exercises)
