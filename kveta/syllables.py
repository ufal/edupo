import re
import sys

class Syllables:

    def __init__(self):
        '''
        Initialize Syllables
        '''
        self.SYLLABLE_PEAKS = "aeiouáéíóúAEORLMBPJKV@"
        self.PEAKS2CHARS = {"a": "a", "e": "e|ě", "i": "i|y|ü", "o": "o|au", "u": "u", "á": "á|aa|à|a", "é": "é|ai|ö|ae|ei|ee|oe|ä|è|e", "í": "í|ý|ü|ie|ee|i|y", "ó": "ó|o", "ú": "ú|ů|ou|u", "A": "au", "E": "eu", "O": "ou", "R": "r", "Ř": "ř", "L": "l", "M": "m", "P": "m", "B": "n", "J": "s", "K": "š", "Y": "z", "V": "ž", "@": "@"}
        self.LONG_PEAKS = "áéíóúAEO"

        self.VOWELS = "aàáäâåeëèéêȩiïìíîoòóöôuùüůúûyýÿæøїаеёиоуыэюя"

    def split_words_to_syllables(self, poem):

        for i, line in enumerate(poem):

            non_syllabic_word = ["", ""]

            for j, word in enumerate(line['words']):

                syllables = []

                fonetic = word['cft']
                ortographic = word['token']
                ortographic_lower = ortographic.lower()
                f_pos = 0
                o_pos = 0
                ph_consonants = ""
                ort_consonants = ""
                while f_pos < len(fonetic):
                    if fonetic[f_pos] in self.SYLLABLE_PEAKS:
                        ph_vowels = fonetic[f_pos]
                        v_options = self.PEAKS2CHARS[ph_vowels].split('|')
                        found = False
                        initial_o_pos = o_pos
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
                                elif v == '@' and o_pos == len(ortographic) - 1:
                                    # pokud je na konci souhláskové skupiny šva
                                    ort_consonants += ortographic[o_pos:]
                                    syllables.append({"ph_consonants": ph_consonants,
                                                      "ph_vowels": ph_vowels,
                                                      "ph_end_consonants": "",
                                                      "ort_consonants": ort_consonants,
                                                      "ort_vowels": "",
                                                      "ort_end_consonants": "",
                                                      "length": 0})
                                    o_pos += len(v)
                                    found = True
                                    ph_consonants = ""
                                    ort_consonants = ""
                                    break
                            if found:
                                break
                            ort_consonants += ortographic[o_pos]
                            o_pos += 1
                        if not found:
                            # Vowel peak couldn't be matched - reset o_pos to avoid consuming the rest of the word
                            # Try to find any vowel character from the VOWELS list instead
                            o_pos = initial_o_pos
                            ort_consonants = ""  # Reset ort_consonants since we're starting over
                            ort_vowels = ""
                            # Skip consonants and collect them
                            while o_pos < len(ortographic) and ortographic_lower[o_pos] not in self.VOWELS:
                                ort_consonants += ortographic[o_pos]
                                o_pos += 1
                            # Collect vowel group if found
                            if o_pos < len(ortographic) and ortographic_lower[o_pos] in self.VOWELS:
                                while o_pos < len(ortographic) and ortographic_lower[o_pos] in self.VOWELS:
                                    ort_vowels += ortographic[o_pos]
                                    o_pos += 1
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
                                ph_consonants = ""
                                ort_consonants = ""
                    else:
                        ph_consonants += fonetic[f_pos]
                    f_pos += 1
                has_merged_non_syllabic = False
                if syllables:
                    syllables[-1]["ph_end_consonants"] = ph_consonants
                    syllables[-1]["ort_end_consonants"] = ortographic[o_pos:]
                    if non_syllabic_word[0] != "":
                        # Don't add trailing punct here - let underscore replacement handle it
                        # to avoid duplication (line 255-256 will use previous word's punct)
                        # Merge accumulated non-syllabic words with current word's first syllable
                        syllables[0]["ph_consonants"] = non_syllabic_word[0] + "_" + syllables[0]["ph_consonants"]
                        syllables[0]["ort_consonants"] = non_syllabic_word[1] + "_" + syllables[0]["ort_consonants"]
                        non_syllabic_word = ["", ""]
                        has_merged_non_syllabic = True
                else:
                    # Accumulate consecutive non-syllabic words with underscore separator
                    word_text = ortographic[o_pos:]
                    # Get punct for current word (to be stored for next iteration)
                    punct_for_word = ""
                    if 'punct' in word and word['punct'].strip():
                        punct_char = word['punct'].strip()
                        # Exclude opening punctuation
                        if punct_char not in ['"', '"', '„', '»', '«', '‹', '›', '(', '[', '{']:
                            punct_for_word = punct_char
                    if non_syllabic_word[0] != "":
                        non_syllabic_word[0] += "_" + ph_consonants
                        # If there's a stored punct from previous word, add it before separator
                        prev_punct = non_syllabic_word[2] if len(non_syllabic_word) > 2 else ""
                        non_syllabic_word[1] = non_syllabic_word[1] + prev_punct + "_" + word_text
                        # Store current word's punct for next iteration
                        non_syllabic_word = [non_syllabic_word[0], non_syllabic_word[1], punct_for_word]
                    else:
                        # First non-syllabic word - store with its punct
                        non_syllabic_word = [ph_consonants, word_text, punct_for_word]



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

                if len(syllables) == 0 and len(fonetic) > 1:
                    
                    print("Splitting to syllables failed:", ortographic, fonetic, file=sys.stderr)
                    
                    # zkusí se triviální dělení po skupinách samohlásek
                    f_pos = 0
                    o_pos = 0
                    ph_consonants = ""
                    ort_consonants = ""
                    while f_pos < len(fonetic):
                        if fonetic[f_pos] in self.SYLLABLE_PEAKS:
                            ph_vowels = fonetic[f_pos]
                            found = False
                            ort_vowels = ""
                            while o_pos < len(ortographic):
                                if ortographic_lower[o_pos] in self.VOWELS:
                                    while o_pos < len(ortographic) and ortographic_lower[o_pos] in self.VOWELS:
                                        ort_vowels += ortographic[o_pos]
                                        o_pos += 1
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
                                    ph_consonants = ""
                                    ort_consonants = ""
                                    break
                                else:
                                    while o_pos < len(ortographic) and not ortographic_lower[o_pos] in self.VOWELS:
                                        ort_consonants += ortographic[o_pos]
                                        o_pos += 1
                        else:
                            ph_consonants += fonetic[f_pos]
                        f_pos += 1
                    if syllables:
                        syllables[-1]["ph_end_consonants"] = ph_consonants
                        syllables[-1]["ort_end_consonants"] = ort_consonants
                        syllables[-1]["ort_end_consonants"] += ortographic[o_pos:]
                # test if the joined syllables equal the original word
                # Skip this check if non-syllabic words were merged (they're part of syllables but not the token)
                if not has_merged_non_syllabic:
                    wfs = ""
                    for syllable in syllables:
                        wfs += syllable['ort_consonants']+syllable['ort_vowels']+syllable['ort_end_consonants']
                    # remove potential non-syllabic preposition
                    if '_' in wfs:
                        wfs = wfs.split('_', 1)[1]
                    if wfs != word['token'] and len(fonetic) > 1:
                        print("WARNING: Syllables do not match the word. Output:", wfs, "Original:", word['token'], "Phonetic: ", fonetic, "Trivial split is used.", file=sys.stderr)
                        syllables = [{"ph_consonants": "",
                                       "ph_vowels": "",
                                       "ph_end_consonants": fonetic,
                                       "ort_consonants": "",
                                       "ort_vowels": "",
                                       "ort_end_consonants": ortographic,
                                       "length": 0}]
                poem[i]['words'][j]['syllables'] = syllables

            # Handle leftover non-syllabic words at end of line
            if non_syllabic_word[0] != "":
                # Find last word with syllables and append to it
                for j in range(len(line['words']) - 1, -1, -1):
                    if line['words'][j]['syllables']:
                        last_syl = line['words'][j]['syllables'][-1]
                        # Add any trailing punct from last non-syllabic word
                        trailing_punct = non_syllabic_word[2] if len(non_syllabic_word) > 2 else ""
                        non_syl_with_punct = non_syllabic_word[1] + trailing_punct
                        # Convert underscores to spaces in accumulated non-syllabic words
                        non_syl_text = non_syl_with_punct.replace('_', ' ')
                        # Don't add space if accumulated text starts with apostrophe (clitic)
                        # Check the original non_syllabic_word[1] before underscore replacement
                        first_char = non_syllabic_word[1].lstrip('_')[0] if non_syllabic_word[1].lstrip('_') else ''
                        if first_char in ['\u2019', '\u2018', "'"]:
                            last_syl["ort_end_consonants"] += non_syl_text
                        else:
                            last_syl["ort_end_consonants"] += " " + non_syl_text
                        break

            # test: join all syllables and compare with text
            text_from_syllables = ""
            for w, word in enumerate(line['words']):
                if 'punct_before' in word:
                    text_from_syllables += word['punct_before']
                for s, syllable in enumerate(word['syllables']):
                    ort_c = syllable['ort_consonants']
                    # If this syllable contains merged text (indicated by _), replace _ with actual punct from previous word
                    if '_' in ort_c and w > 0 and not line['words'][w-1]['syllables']:
                        # Previous word had no syllables and was merged; use its punct instead of just space
                        prev_punct = line['words'][w-1].get('punct', ' ')
                        ort_c = ort_c.replace('_', prev_punct)
                    else:
                        ort_c = ort_c.replace('_', ' ')
                    text_from_syllables += ort_c + syllable['ort_vowels'] + syllable['ort_end_consonants']
                # Only add punct if word has syllables (words without syllables have punct handled via underscore replacement)
                if word['syllables'] and 'punct' in word:
                    text_from_syllables += word['punct']
            original_text = line['text']
            if text_from_syllables != original_text:
                print("WARNING: different text in syllables:", text_from_syllables, "vs.", original_text, file=sys.stderr)
        return poem

