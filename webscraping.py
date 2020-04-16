#! python3

# webscraping.py - Handles scraping from websites and processing the html

import re
import mwclient
import wikitextparser as wtp

########################################################
############## Wikitionary parsing #####################
########################################################

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
