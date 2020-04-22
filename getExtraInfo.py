from webscraping import WikitionaryParser
from pyperclip import copy, paste

word = paste()
wikiParser = WikitionaryParser(word)
extraInfo = wikiParser.getWordForms() + wikiParser.getIpa()
copy(extraInfo.replace("<br>", "\n"))
