#! python3

# webscraping.py - Handles scraping from websites and processing the html

import re

########################################################
############## Wikitionary parsing #####################
########################################################

import mwclient
import wikitextparser as wtp

class WikitionaryParser(object):
    """docstring for WikitionaryParser."""

    def __init__(self, word):
        super(WikitionaryParser, self).__init__()
        site = mwclient.Site('de.wiktionary.org/')
        page = site.pages[word]
        self.text = page.text()
        parsed = wtp.parse(self.text)
        self.templates = parsed.templates

    def _getArguments(self, name):
        arguments = []
        for template in self.templates:
            if template.name == name:
                arguments = template.arguments
                break
        return arguments

    def _getGender(self):
        for template in self.templates:
            if template.name == "m":
                gender = "der "
                break
            if template.name == "f":
                gender = "die "
                break
            if template.name == "m":
                gender = "das "
                break
        return gender

    def _getWordType(self):
        arguments = self._getArguments("Wortart")
        wordType = arguments[0].value
        return wordType

    def _isNoun(self):
        return self._getWordType() == "Substantiv"

    def _isVerb(self):
        return self._getWordType() == "Verb"

    def _getRawWordForms(self):
        substring = self.text.split("Worttrennung", 1)[1]
        substring = substring.split(":", 1)[1]
        substring = substring.split("\n", 1)[0]
        return substring

    def getIpa(self):
        arguments = self._getArguments("Lautschrift")
        ipa = arguments[0].value
        return ipa

    def getWordForms(self):
        wordForms = ""
        if self._isNoun():
            rawWordForms = self._getRawWordForms()
            singular = rawWordForms.split(",")[0]
            plural = rawWordForms.split("} ")[1]
            gender = self._getGender()
            wordForms = gender + singular + "<br>" + plural + "<br>"
        if self._isVerb():
            rawWordForms = self._getRawWordForms()
            infinitif = rawWordForms.split(",")[0]
            praeterutum = rawWordForms.split("Prät.}} ")[1].split(",")[0]
            partizip = rawWordForms.split("Part.}} ")[1]
            wordForms = infinitif + "<br>" + praeterutum + "<br>" + partizip + "<br>"
        return wordForms

########################################################
################ German.net parsing ####################
########################################################
import pprint as pp

DROPDOWN = 0
BLANK = 1

def getExerciseBox(soup):
    exerciseBox = soup.find("div", {"class": "exercisebox"})
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

def getItems(soup, answerFormat):
    exerciseBox = getExerciseBox(soup)
    if answerFormat == BLANK:
        items = exerciseBox.select(".resultbox2")
    elif answerFormat == DROPDOWN:
        items = exerciseBox.find_all("select", class_="textbox")
    return items

def parseComponents(item):
    rawText1 = item.previous_sibling
    rawText2 = item.next_sibling
    text1 = rawText1.split(")")[1].strip()
    text2 = rawText2.strip()
    component = [text1, text2]
    return component

def getSentenceComponents(soup, answerFormat):
    components = []
    items = getItems(soup, answerFormat)
    for item in items:
        component = parseComponents(item)
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

def getDropdownOptions(menu):
    optionsSoup = menu.find_all("option")[1:]
    options = ""
    for option in optionsSoup:
        options += option.text + ", "
    return(options)

def getHints(soup, answerFormat):
    hints = []
    if answerFormat == BLANK:
        hintSoup = soup.find_all("span", class_="hint_text")
        i = 0
        for form in hintSoup:
            text = form.text
            if text is not "":
                if i == 0:
                    i = 1
                    continue
                hints.append(text)
    elif answerFormat == DROPDOWN:
        dropdownMenus = soup.find_all("select", class_="textbox")
        for menu in dropdownMenus:
            options = getDropdownOptions(menu)
            hints.append(options)
    return(hints)

def getParsedExercises(exerciseSoup, solutionSoup, answerFormat):
    answers = getAnswers(solutionSoup)
    hints = getHints(exerciseSoup, answerFormat)
    sentenceComponents = getSentenceComponents(exerciseSoup, answerFormat)
    fullSentences = getFullSentences(sentenceComponents, answers)
    blankedSentences = getSentencesWithBlanks(fullSentences, answers)

    exercises = {
        "frontBlanked": blankedSentences,
        "hint": hints,
        "answer": answers,
        "fullSentence": fullSentences
                }
    import pprint
    pprint.pprint(exercises)
    assert(len(answers) == len(fullSentences))
    assert(len(answers) == len(blankedSentences))
    assert(len(answers) == len(hints))

    return(exercises)
