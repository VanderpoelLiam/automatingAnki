#! python3

# getExtraInfo.py - Copys verb/noun forms and IPA of a word to the clipboard

import sys
from pyperclip import copy, paste
from webscraping import getSoup, getIpa, getWordClass, getWordForms, isVerb, isNoun

WIKITIONARY = 'https://de.wiktionary.org/wiki/'
extraInfo = ""

def getWord():
    if len(sys.argv) > 1:
        word = sys.argv[1]
    else:
        word = paste()
    return(word)

word = getWord()
wikitionarySite = WIKITIONARY + word
wiktionarySoup = getSoup(wikitionarySite)
wordClass = getWordClass(wiktionarySoup)

if isVerb(wordClass) or isNoun(wordClass):
    extraInfo = getWordForms(wiktionarySoup, wordClass)

extraInfo += getIpa(wiktionarySoup)
copy(extraInfo)
