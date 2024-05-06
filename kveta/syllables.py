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
                        syllables.append({"ph_consonants": c, "ph_vowel": v})
                    elif len(cv) > 0 and len(syllables) > 0 : # it is the last consonant group in the word, add it to the previous syllable
                        syllables[-1]["ph_end_consonants"] = cv

                # map syllable peaks back to the characters
                current_position = 0
                lc_word = word["token"].lower()
                for ii, s in enumerate(syllables):
                    chars = self.PEAKS2CHARS[s["ph_vowel"]].split('|')
                    consonants = ""
                    vowels = ""
                    end_consonants = ""
                    while current_position < len(lc_word) and lc_word[current_position] not in chars and lc_word[current_position:current_position + 1] not in chars:
                        consonants += word["token"][current_position]
                        current_position += 1
                    if current_position < len(lc_word):
                        vowels = word["token"][current_position]
                        current_position += 1
                        if s["ph_vowel"] in ["A", "E", "O"]:
                            vowels = word["token"][current_position]
                            current_position += 1
                    syllables[ii]['ort_consonants'] = consonants
                    syllables[ii]['ort_vowel'] = vowels
                    if "ph_end_consonants" in s:
                        end_consonants = word["token"][current_position:]
                        syllables[ii]['ort_end_consonants'] = end_consonants
                    length = 0
                    if s["ph_vowel"] in self.LONG_PEAKS:
                        length = 1
                    syllables[ii]["length"] = length

                poem[i]['words'][j]['syllables'] = syllables

        return poem

