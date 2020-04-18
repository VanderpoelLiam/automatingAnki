#! python3

# germanGenderIndicators.py - Detects indicators of the gender of German nouns

import re
# https://en.wikipedia.org/wiki/German_declension
# TODO: regex for decline like der i.e. all-, dies-, jed-, jen-, manch-, solch-, welch-
# TODO: regex for decline like ein i.e. kein-, dein-, ihr-, euer-
# TODO: test all definite articles
# TODO: test one of each decline like ...

indefiniteRegex = r"\b[Ee]in(e|en|em|es|er)?\b(?:\s+\w+)?\s+"

def getGenderIndicator(sentence, noun):
    match = re.search(indefiniteRegex + noun, sentence)
    indicator = re.sub(" " + noun, "", match.group())
    return indicator

def numWordsInStr(str):
    return len(re.split(" ", str))

def removeAdjectiveDeclination(adjective):
    regex = r"(e|er|en|em|es)\b"
    adjective = re.sub(regex, "", adjective)
    return adjective

def getIndicatorReplacement(indicator):
    replacementAdjective = ""

    if numWordsInStr(indicator) > 1:
        indicator, adjective = re.split(" ", indicator)
        replacementAdjective = " " + removeAdjectiveDeclination(adjective)

    replacementIndicator = "ein"

    replacement = replacementIndicator + replacementAdjective
    return "(" + replacement + ")"

def removeGenderIndicator(sentence, noun):
    indicator = getGenderIndicator(sentence, noun)
    replacement = getIndicatorReplacement(indicator)
    sentenceRemovedGender = sentence.replace(indicator + " " + noun,
                                             replacement + " " + noun)
    return sentenceRemovedGender

import unittest

class TestGermanGenderIndicators(unittest.TestCase):

    def test_ein(self):
        noun = "Buch"
        sentence = "Sie dürfen ein beliebiges Buch lesen."
        indicator = "ein beliebiges"
        replacement = "(ein beliebig)"
        expected = "Sie dürfen (ein beliebig) Buch lesen."

        self.assertEqual(getGenderIndicator(sentence, noun), indicator)
        self.assertEqual(getIndicatorReplacement(indicator), replacement)
        self.assertEqual(removeGenderIndicator(sentence, noun), expected)

    def test_einer(self):
        noun = "Wohnung"
        sentence = "einer Damals wohten oft mehrere Familien in einer Wohnung."
        indicator = "einer"
        replacement = "(ein)"
        expected = "einer Damals wohten oft mehrere Familien in (ein) Wohnung."

        self.assertEqual(getGenderIndicator(sentence, noun), indicator)
        self.assertEqual(getIndicatorReplacement(indicator), replacement)
        self.assertEqual(removeGenderIndicator(sentence, noun), expected)

    def test_eine(self):
        noun = "Aktion"
        sentence = "Da kann man so eine Aktion im Grunde gleich sein lassen."
        indicator = "eine"
        replacement = "(ein)"
        expected = "Da kann man so (ein) Aktion im Grunde gleich sein lassen."

        self.assertEqual(getGenderIndicator(sentence, noun), indicator)
        self.assertEqual(getIndicatorReplacement(indicator), replacement)
        self.assertEqual(removeGenderIndicator(sentence, noun), expected)

    def test_einen(self):
        noun = "Film"
        sentence = "Ihr dürft einen Film sehen"
        indicator = "einen"
        replacement = "(ein)"
        expected = "Ihr dürft (ein) Film sehen"

        self.assertEqual(getGenderIndicator(sentence, noun), indicator)
        self.assertEqual(getIndicatorReplacement(indicator), replacement)
        self.assertEqual(removeGenderIndicator(sentence, noun), expected)

    def test_einem(self):
        noun = "Arzt"
        sentence = "Ein Gespräch zwischen einem Arzt und einem Patienten muss immer vertraulich sein."
        indicator = "einem"
        replacement = "(ein)"
        expected = "Ein Gespräch zwischen (ein) Arzt und einem Patienten muss immer vertraulich sein."

        self.assertEqual(getGenderIndicator(sentence, noun), indicator)
        self.assertEqual(getIndicatorReplacement(indicator), replacement)
        self.assertEqual(removeGenderIndicator(sentence, noun), expected)

    def test_eines(self):
        noun = "Abends"
        sentence = "hat mich eines Abends auf seine herrliche Terrasse gelockt"
        indicator = "eines"
        replacement = "(ein)"
        expected = "hat mich (ein) Abends auf seine herrliche Terrasse gelockt"

        self.assertEqual(getGenderIndicator(sentence, noun), indicator)
        self.assertEqual(getIndicatorReplacement(indicator), replacement)
        self.assertEqual(removeGenderIndicator(sentence, noun), expected)

    # def test_mein(self):
    #     noun = "Name"
    #     sentence = "Mein Name hat 5 Buchstaben"
    #     indicator = "Mein"
    #     replacement = "(Mein)"
    #     expected = "(Mein) Name hat 5 Buchstaben"
    #
    #     self.assertEqual(getGenderIndicator(sentence, noun), indicator)
    #     self.assertEqual(getIndicatorReplacement(indicator), replacement)
    #     self.assertEqual(removeGenderIndicator(sentence, noun), expected)
    #
    # def test_meinen(self):
    #     noun = "Namen"
    #     sentence = "Ich sagte meinen Namen"
    #     indicator = "meinen"
    #     replacement = "(mein)"
    #     expected = "Ich sagte (mein) Namen"
    #
    #     self.assertEqual(getGenderIndicator(sentence, noun), indicator)
    #     self.assertEqual(getIndicatorReplacement(indicator), replacement)
    #     self.assertEqual(removeGenderIndicator(sentence, noun), expected)
    #
    # def test_des(self):
    #     noun = "Buches"
    #     sentence = "Die Zukunft des Buches ist schwer"
    #     indicator = "des"
    #     replacement = "(de...)"
    #     expected = "Die Zukunft (de...) Buches ist schwer"
    #
    #     self.assertEqual(getGenderIndicator(sentence, noun), indicator)
    #     self.assertEqual(getIndicatorReplacement(indicator), replacement)
    #     self.assertEqual(removeGenderIndicator(sentence, noun), expected)


if __name__ == '__main__':
    unittest.main()
