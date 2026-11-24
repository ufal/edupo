"""
Utility functions for poem processing.

Low-level helpers for metre selection, rhyme annotation, stanza separation, etc.
"""

import sys
from collections import defaultdict


# Constants
METRE_PRIORITY = defaultdict(int)
METRE_PRIORITY['T'] = 5
METRE_PRIORITY['J'] = 4
METRE_PRIORITY['D'] = 3
METRE_PRIORITY['A'] = 2
METRE_PRIORITY['N'] = -1


def dict_factory(cursor, row):
    """Convert SQLite row to dictionary."""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def add_rhyme_annotation(poem, warnings=None):
    """Add rhyme annotation to poem syllables.

    Marks, on the last syllabic word of each verse (and possibly the one before
    it), which syllables the rhyme is taken from ('v' = from the vowel, 'c' =
    from the consonant). Words without syllables (punctuation-only tokens,
    numbers, ...) at the end of the verse are skipped.

    Args:
        poem: list of verse dicts from Kveta
        warnings: optional list to collect warning strings; if None, prints to stderr
    """
    def warn(msg):
        if warnings is not None:
            warnings.append(msg)
        else:
            print(msg, file=sys.stderr)

    for verse in poem:
        words = verse.get("words") or []
        syllabic = [i for i, w in enumerate(words) if w.get("syllables")]
        if not syllabic:
            warn(f"WARNING: No words/syllables in verse, skipping rhyme annotation: {repr(verse['text'])}")
            continue
        if syllabic[-1] != len(words) - 1:
            warn(f"WARNING: No syllables for the last word: {repr(verse['text'])}")

        last = words[syllabic[-1]]
        # the two-word rhyme is only considered for the word directly before the last
        # syllabic one (a vowel-less token in between, e.g. the preposition "v", breaks it)
        penultimate = words[syllabic[-2]] if len(syllabic) >= 2 and syllabic[-2] == syllabic[-1] - 1 else None
        last_vec = last.get("vec") or {}
        pen_vec = (penultimate.get("vec") or {}) if penultimate is not None else {}

        if len(last["syllables"]) >= 2:  # multi-syllable word
            last["syllables"][-2]["rhyme_from"] = 'v'
            last["syllables"][-1]["rhyme_from"] = 'c'
        elif penultimate is not None and pen_vec and (
                pen_vec.get("prep", [0])[0] == 1 or last_vec.get("content", [1])[0] == 0):
            # monosyllable after a preposition, or a function word: rhyme spans two words
            penultimate["syllables"][-1]["rhyme_from"] = 'v'
            last["syllables"][-1]["rhyme_from"] = 'c'
        elif last["syllables"][-1]["ph_end_consonants"]:
            last["syllables"][-1]["rhyme_from"] = 'v'
        else:
            if last["syllables"][-1]['ph_consonants']:
                last["syllables"][-1]["rhyme_from"] = 'c'
            else:
                last["syllables"][-1]["rhyme_from"] = 'v'


def get_rhyming_part(syllables):
    """Extract the rhyming part from syllables."""
    r_end = ""
    for i, syllable in enumerate(syllables):
        if syllable['rhyme_from'] == 'c':
            # [-1:] not [-1]: the consonant string can be empty
            r_end += (syllable['ort_consonants'][-1:] if i == 0 else syllable['ort_consonants']) + syllable['ort_vowels'] + syllable['ort_end_consonants']
        elif syllable['rhyme_from'] == 'v':
            r_end += syllable['ort_vowels'] + syllable['ort_end_consonants']
        elif syllable['rhyme_from'] == 'ec':
            r_end += syllable['end_consonants'][-1:] if i == 0 else syllable['end_consonants']
        else:
            raise ValueError(f"Invalid rhyme_from value {syllable['rhyme_from']}")
    return r_end


def select_metre(metres):
    """Select the dominant metre from a list ('N' = unknown when the list is empty)."""
    if not metres:
        return 'N'
    return max(metres, key=lambda m: METRE_PRIORITY[m])


def separate_stanzas(poem):
    """Separate poem into stanzas."""
    stanzas = []
    current_stanza = []
    stanza_num = None
    for verse in poem:
        if verse['stanza'] != stanza_num:
            if current_stanza:
                stanzas.append(current_stanza)
            current_stanza = []
            stanza_num = verse['stanza']
        current_stanza.append(verse)
    if current_stanza:
        stanzas.append(current_stanza)
    return stanzas
