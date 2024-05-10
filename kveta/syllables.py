import re

class Syllables:

    def __init__(self):
        '''
        Initialize Syllables
        '''
        self.SYLLABLE_PEAKS = "aeiouáéíóúAEORLBP"
        self.PEAKS2CHARS = {"a": "a", "e": "e|ě", "i": "i|y", "o": "o", "u": "u", "á": "á", "é": "é", "í": "í|ý", "ó": "ó", "ú": "ú|ů", "A": "au", "E": "eu", "O": "ou", "R": "r", "L": "l", "P": "m", "B": "n"}
        self.LONG_PEAKS = "áéíóúAEO"

    def split_words_to_syllables(self, poem):

        for i, line in enumerate(poem):

            non_syllabic_word = ["", ""]

            for j, word in enumerate(line['words']):

                syllables = []

                fonetic = word['cft']
                ortographic = word['token']
                ortographic_lower = word['token'].lower()
                f_pos = 0
                o_pos = 0
                ph_consonants = ""
                ort_consonants = ""
                while f_pos < len(fonetic):
                    if fonetic[f_pos] in self.SYLLABLE_PEAKS:
                        ph_vowels = fonetic[f_pos]
                        v_options = self.PEAKS2CHARS[ph_vowels].split('|')
                        found = False
                        while o_pos < len(ortographic):
                            for v in v_options:
                                if ortographic_lower[o_pos:o_pos+len(v)] == v:
                                    ort_vowels = ortographic[o_pos:o_pos+len(v)]
                                    length = 0
                                    if ph_vowels in self.LONG_PEAKS:
                                        length = 1
                                    syllables.append({"ph_consonants": ph_consonants,
                                                      "ph_vowels": ph_vowels,
                                                      "ph_end_consonants": "",
                                                      "ort_consonants": ort_consonants,
                                                      "ort_vowels": ort_vowels,
                                                      "ort_end_consonants": "",
                                                      "length": length})
                                    o_pos += len(v)
                                    found = True
                                    ph_consonants = ""
                                    ort_consonants = ""
                                    break
                            if found:
                                break
                            ort_consonants += ortographic[o_pos]
                            o_pos += 1
                    else:
                        ph_consonants += fonetic[f_pos]
                    f_pos += 1
                if syllables:
                    syllables[-1]["ph_end_consonants"] = ph_consonants
                    syllables[-1]["ort_end_consonants"] = ortographic[o_pos:]
                    if non_syllabic_word[0] != "":
                        syllables[0]["ph_consonants"] = non_syllabic_word[0] + "_" + syllables[0]["ph_consonants"]
                        syllables[0]["ort_consonants"] = non_syllabic_word[1] + "_" + syllables[0]["ort_consonants"]
                        non_sylabic_word = ["", ""]
                else:
                    non_syllabic_word = [ph_consonants, ortographic[o_pos:]]



                #fonetic = re.sub(r"([" + self.SYLLABLE_PEAKS + "])", r"#\1@", fonetic)
                #for cv in fonetic.split("@"):
                #    if '#' in cv: # if there is a syllable peak 
                #        c, v = cv.split("#")
                #        syllables.append({"ph_consonants": c, "ph_vowel": v})
                #    elif len(cv) > 0 and len(syllables) > 0 : # it is the last consonant group in the word, add it to the previous syllable
                #        syllables[-1]["ph_end_consonants"] = cv

                # map syllable peaks back to the characters
                #current_position = 0
                #lc_word = word["token"].lower()
                #for ii, s in enumerate(syllables):
                #    chars = self.PEAKS2CHARS[s["ph_vowel"]].split('|')
                #    consonants = ""
                #    vowels = ""
                #    end_consonants = ""
                #    while current_position < len(lc_word) and lc_word[current_position] not in chars and lc_word[current_position:current_position + 1] not in chars:
                #        consonants += word["token"][current_position]
                #        current_position += 1
                #    if current_position < len(lc_word):
                #        vowels = word["token"][current_position]
                #        current_position += 1
                #        if s["ph_vowel"] in ["A", "E", "O"]:
                #            vowels = word["token"][current_position]
                #            current_position += 1
                #    syllables[ii]['ort_consonants'] = consonants
                #    syllables[ii]['ort_vowel'] = vowels
                #    if "ph_end_consonants" in s:
                #        end_consonants = word["token"][current_position:]
                #        syllables[ii]['ort_end_consonants'] = end_consonants
                #    length = 0
                #    if s["ph_vowel"] in self.LONG_PEAKS:
                #        length = 1
                #    syllables[ii]["length"] = length

                poem[i]['words'][j]['syllables'] = syllables

        return poem

