#! python3

# germanGenderIndicators.py - Detects indicators of the gender of German nouns


import re

class NounSentence(object):
    """docstring for NounSentence."""
    matchAdj = r"(?:\s+\w+)?\s+"
    adjDecl = r"(e|er|en|em|es)\b"
    indefDecl = "(e|en|em|es|er)"
    defDecl = "(er|en|em|es|ie|as)"

    indefBeg = "([Mm]|[Ss]|[Dd]|[Kk])?[Ee]in"
    indefRegex = r"\b" + indefBeg + indefDecl + r"?\b" + matchAdj

    possesBeg = "([Ee]uer|[Ii]hr|[Uu]nser)"
    possesRegex = r"\b" + possesBeg + indefDecl + r"?\b" + matchAdj

    defBeg = "([Dd]|[Dd]ies)"
    defRegex = r"\b" + defBeg + defDecl + r"?\b" + matchAdj

    def __init__(self, noun, sentence):
        super(NounSentence, self).__init__()
        self.noun = noun
        self.sentence = sentence

    def _numWordsInStr(self, str):
        return len(re.split(" ", str))

    def _setGenderIndicator(self):
        match = re.search(self.indefRegex + self.noun, self.sentence)
        if match is None:
            match = re.search(self.defRegex + self.noun, self.sentence)
        if match is None:
            match = re.search(self.possesRegex + self.noun, self.sentence)
        if match is None:
            raise Exception("No gender indicator found.")

        self.matchStr = re.sub(" " + self.noun, "", match.group())

        if self._numWordsInStr(self.matchStr) > 1:
            self.indicator, self.adjective = re.split(" ", self.matchStr)
        else:
            self.indicator = self.matchStr
            self.adjective = ""

    def _removeAdjectiveDeclination(self):
        return re.sub(self.adjDecl, "", self.adjective)

    def _removeIndicatorDeclination(self):
        match = re.search("[Ee]in", self.indicator)
        if match is not None:
            return re.sub(self.indefDecl + r"\b", "", self.indicator)

        match = re.search(self.possesBeg, self.indicator)
        if match is not None:
            return match.group()

        match = re.search("[Dd]", self.indicator)
        if match is not None:
            return re.sub(self.defDecl + r"\b", "-", self.indicator)

        raise Exception("Could not remove indicator declination.")

    def _setReplacement(self):
        if self.adjective != "":
            replacementAdjective = " " + self._removeAdjectiveDeclination()
            replacementIndicator = self._removeIndicatorDeclination()
            replacement = replacementIndicator + replacementAdjective
        else:
            replacement = self._removeIndicatorDeclination()

        self.replacement = "(" + replacement + ")"

    def removeGenderIndicator(self):
        self._setGenderIndicator()
        self._setReplacement()
        sentenceRemovedGender = self.sentence.replace(self.matchStr + " " + self.noun,
                                                      self.replacement + " " + self.noun)
        return sentenceRemovedGender


import unittest

class TestGermanGenderIndicators(unittest.TestCase):

    def test_ein(self):
        noun = "Buch"
        sentence = "Sie dürfen ein beliebiges Buch lesen."
        indicator = "ein"
        replacement = "(ein beliebig)"
        expected = "Sie dürfen (ein beliebig) Buch lesen."

        testObj = NounSentence(noun, sentence)
        testObj._setGenderIndicator()
        testObj._setReplacement()

        self.assertEqual(testObj.indicator, indicator)
        self.assertEqual(testObj.replacement, replacement)
        self.assertEqual(testObj.removeGenderIndicator(), expected)

    def test_einer(self):
        noun = "Wohnung"
        sentence = "Damals wohten oft mehrere Familien in einer Wohnung."
        indicator = "einer"
        replacement = "(ein)"
        expected = "Damals wohten oft mehrere Familien in (ein) Wohnung."

        testObj = NounSentence(noun, sentence)
        testObj._setGenderIndicator()
        testObj._setReplacement()

        self.assertEqual(testObj.indicator, indicator)
        self.assertEqual(testObj.replacement, replacement)
        self.assertEqual(testObj.removeGenderIndicator(), expected)

    def test_eine(self):
        noun = "Aktion"
        sentence = "Da kann man so eine Aktion im Grunde gleich sein lassen."
        indicator = "eine"
        replacement = "(ein)"
        expected = "Da kann man so (ein) Aktion im Grunde gleich sein lassen."

        testObj = NounSentence(noun, sentence)
        testObj._setGenderIndicator()
        testObj._setReplacement()

        self.assertEqual(testObj.indicator, indicator)
        self.assertEqual(testObj.replacement, replacement)
        self.assertEqual(testObj.removeGenderIndicator(), expected)

    def test_einen(self):
        noun = "Film"
        sentence = "Ihr dürft einen Film sehen"
        indicator = "einen"
        replacement = "(ein)"
        expected = "Ihr dürft (ein) Film sehen"

        testObj = NounSentence(noun, sentence)
        testObj._setGenderIndicator()
        testObj._setReplacement()

        self.assertEqual(testObj.indicator, indicator)
        self.assertEqual(testObj.replacement, replacement)
        self.assertEqual(testObj.removeGenderIndicator(), expected)

    def test_einem(self):
        noun = "Arzt"
        sentence = "Ein Gespräch zwischen einem Arzt und einem Patienten muss immer vertraulich sein."
        indicator = "einem"
        replacement = "(ein)"
        expected = "Ein Gespräch zwischen (ein) Arzt und einem Patienten muss immer vertraulich sein."

        testObj = NounSentence(noun, sentence)
        testObj._setGenderIndicator()
        testObj._setReplacement()

        self.assertEqual(testObj.indicator, indicator)
        self.assertEqual(testObj.replacement, replacement)
        self.assertEqual(testObj.removeGenderIndicator(), expected)

    def test_eines(self):
        noun = "Abends"
        sentence = "hat mich eines Abends auf seine herrliche Terrasse gelockt"
        indicator = "eines"
        replacement = "(ein)"
        expected = "hat mich (ein) Abends auf seine herrliche Terrasse gelockt"

        testObj = NounSentence(noun, sentence)
        testObj._setGenderIndicator()
        testObj._setReplacement()

        self.assertEqual(testObj.indicator, indicator)
        self.assertEqual(testObj.replacement, replacement)
        self.assertEqual(testObj.removeGenderIndicator(), expected)

    def test_der(self):
        noun = "Klasse"
        sentence = "Der Student steht hinten in der Klasse."
        indicator = "der"
        replacement = "(d-)"
        expected = "Der Student steht hinten in (d-) Klasse."

        testObj = NounSentence(noun, sentence)
        testObj._setGenderIndicator()
        testObj._setReplacement()

        self.assertEqual(testObj.indicator, indicator)
        self.assertEqual(testObj.replacement, replacement)
        self.assertEqual(testObj.removeGenderIndicator(), expected)

    def test_den(self):
        noun = "Gewürzen"
        sentence = "Mit den passenden Gewürzen wird dieser Auflauf sehr gut schmecken."
        indicator = "den"
        replacement = "(d- passend)"
        expected = "Mit (d- passend) Gewürzen wird dieser Auflauf sehr gut schmecken."

        testObj = NounSentence(noun, sentence)
        testObj._setGenderIndicator()
        testObj._setReplacement()

        self.assertEqual(testObj.indicator, indicator)
        self.assertEqual(testObj.replacement, replacement)
        self.assertEqual(testObj.removeGenderIndicator(), expected)

    def test_dem(self):
        noun = "Regen"
        sentence = "Ihr Regenschirm schützt Sie vor dem Regen."
        indicator = "dem"
        replacement = "(d-)"
        expected = "Ihr Regenschirm schützt Sie vor (d-) Regen."

        testObj = NounSentence(noun, sentence)
        testObj._setGenderIndicator()
        testObj._setReplacement()

        self.assertEqual(testObj.indicator, indicator)
        self.assertEqual(testObj.replacement, replacement)
        self.assertEqual(testObj.removeGenderIndicator(), expected)

    def test_des(self):
        noun = "Spiels"
        sentence = "Die Spannung während des Spiels war unglaublich."
        indicator = "des"
        replacement = "(d-)"
        expected = "Die Spannung während (d-) Spiels war unglaublich."

        testObj = NounSentence(noun, sentence)
        testObj._setGenderIndicator()
        testObj._setReplacement()

        self.assertEqual(testObj.indicator, indicator)
        self.assertEqual(testObj.replacement, replacement)
        self.assertEqual(testObj.removeGenderIndicator(), expected)

    def test_die(self):
        noun = "Firma"
        sentence = "Die Firma wirbt für ihre Produkte."
        indicator = "Die"
        replacement = "(D-)"
        expected = "(D-) Firma wirbt für ihre Produkte."

        testObj = NounSentence(noun, sentence)
        testObj._setGenderIndicator()
        testObj._setReplacement()

        self.assertEqual(testObj.indicator, indicator)
        self.assertEqual(testObj.replacement, replacement)
        self.assertEqual(testObj.removeGenderIndicator(), expected)

    def test_das(self):
        noun = "Buch"
        sentence = "Das Buch, dessen Autor unbekannt ist."
        indicator = "Das"
        replacement = "(D-)"
        expected = "(D-) Buch, dessen Autor unbekannt ist."

        testObj = NounSentence(noun, sentence)
        testObj._setGenderIndicator()
        testObj._setReplacement()

        self.assertEqual(testObj.indicator, indicator)
        self.assertEqual(testObj.replacement, replacement)
        self.assertEqual(testObj.removeGenderIndicator(), expected)

    def test_mein(self):
        noun = "Name"
        sentence = "Mein Name hat 5 Buchstaben"
        indicator = "Mein"
        replacement = "(Mein)"
        expected = "(Mein) Name hat 5 Buchstaben"

        testObj = NounSentence(noun, sentence)
        testObj._setGenderIndicator()
        testObj._setReplacement()

        self.assertEqual(testObj.indicator, indicator)
        self.assertEqual(testObj.replacement, replacement)
        self.assertEqual(testObj.removeGenderIndicator(), expected)

    def test_kein(self):
        noun = "Namen"
        sentence = "Ich sagte keinen Namen"
        indicator = "keinen"
        replacement = "(kein)"
        expected = "Ich sagte (kein) Namen"

        testObj = NounSentence(noun, sentence)
        testObj._setGenderIndicator()
        testObj._setReplacement()

        self.assertEqual(testObj.indicator, indicator)
        self.assertEqual(testObj.replacement, replacement)
        self.assertEqual(testObj.removeGenderIndicator(), expected)

    def test_dein(self):
        noun = "Tasche"
        sentence = "Das ist deine Tasche."
        indicator = "deine"
        replacement = "(dein)"
        expected = "Das ist (dein) Tasche."

        testObj = NounSentence(noun, sentence)
        testObj._setGenderIndicator()
        testObj._setReplacement()

        self.assertEqual(testObj.indicator, indicator)
        self.assertEqual(testObj.replacement, replacement)
        self.assertEqual(testObj.removeGenderIndicator(), expected)

    def test_ihr(self):
        noun = "Angelegenheit"
        sentence = "Das ist ihre Angelegenheit."
        indicator = "ihre"
        replacement = "(ihr)"
        expected = "Das ist (ihr) Angelegenheit."

        testObj = NounSentence(noun, sentence)
        testObj._setGenderIndicator()
        testObj._setReplacement()

        self.assertEqual(testObj.indicator, indicator)
        self.assertEqual(testObj.replacement, replacement)
        self.assertEqual(testObj.removeGenderIndicator(), expected)

    def test_euer(self):
        noun = "Plan"
        sentence = "Das ist euer Plan."
        indicator = "euer"
        replacement = "(euer)"
        expected = "Das ist (euer) Plan."

        testObj = NounSentence(noun, sentence)
        testObj._setGenderIndicator()
        testObj._setReplacement()

        self.assertEqual(testObj.indicator, indicator)
        self.assertEqual(testObj.replacement, replacement)
        self.assertEqual(testObj.removeGenderIndicator(), expected)

    def test_sein(self):
        noun = "Löffel"
        sentence = "Das ist sein Löffel. "
        indicator = "sein"
        replacement = "(sein)"
        expected = "Das ist (sein) Löffel. "

        testObj = NounSentence(noun, sentence)
        testObj._setGenderIndicator()
        testObj._setReplacement()

        self.assertEqual(testObj.indicator, indicator)
        self.assertEqual(testObj.replacement, replacement)
        self.assertEqual(testObj.removeGenderIndicator(), expected)

    def test_unser(self):
        noun = "Angelegenheit"
        sentence = "Das ist unsere Angelegenheit. "
        indicator = "unsere"
        replacement = "(unser)"
        expected = "Das ist (unser) Angelegenheit. "

        testObj = NounSentence(noun, sentence)
        testObj._setGenderIndicator()
        testObj._setReplacement()

        self.assertEqual(testObj.indicator, indicator)
        self.assertEqual(testObj.replacement, replacement)
        self.assertEqual(testObj.removeGenderIndicator(), expected)

    def test_dies(self):
        noun = "Fall"
        sentence = "In diesem Fall ist besondere Vorsicht geboten."
        indicator = "diesem"
        replacement = "(dies-)"
        expected = "In (dies-) Fall ist besondere Vorsicht geboten."

        testObj = NounSentence(noun, sentence)
        testObj._setGenderIndicator()
        testObj._setReplacement()

        self.assertEqual(testObj.indicator, indicator)
        self.assertEqual(testObj.replacement, replacement)
        self.assertEqual(testObj.removeGenderIndicator(), expected)


# if __name__ == '__main__':
#     unittest.main()
