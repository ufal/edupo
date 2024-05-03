import re

class Syllables:

    def __init__(self):
        '''
        Initialize Syllables
        '''
        self.SYLLABLE_PEAKS = "aeiouáéíóúAEORLBP" # cft
        self.PEAKS2CHARS = {"a": "a", "e": "e|ě", "i": "i|y", "o": "o", "u": "u", "á": "á", "é": "é", "í": "í|ý", "ó": "ó", "ú": "ú|ů", "A": "au", "E": "eu", "O": "ou", "R": "r", "L": "l", "P": "m", "B": "n"}
        self.LONG_PEAKS = "áéíóúAEO"

    def split_words_to_syllables(self, poem):

        for i, line in enumerate(poem):

            for j, word in enumerate(line['words']):

                syllables = []

                fonetic = word['cft']
                fonetic = re.sub(r"([" + self.SYLLABLE_PEAKS + "])", r"#\1@", fonetic)
                for cv in fonetic.split("@"):
                    if '#' in cv: # if there is a syllable peak 
                        c, v = cv.split("#")
                        length = 0
                        if v in self.LONG_PEAKS:
                            length = 1
                        syllables.append({"consonants": c, "vowel": v, "length": length})
                    elif len(cv) > 0 and len(syllables) > 0 : # it is the last consonant group in the word, add it to the previous syllable
                        syllables[-1]["end_consonants"] = cv

                # map syllable peaks back to the characters
                current_position = 0
                lc_word = word["token"].lower()
                for ii, s in enumerate(syllables):
                    chars = self.PEAKS2CHARS[s["vowel"]].split('|')
                    while current_position < len(lc_word) and lc_word[current_position] not in chars:
                        current_position += 1
                    syllables[ii]['charmap'] = current_position

                poem[i]['words'][j]['syllables'] = syllables

        return poem

