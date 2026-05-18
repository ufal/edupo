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

    Args:
        poem: list of verse dicts from Kveta
        warnings: optional list to collect warning strings; if None, prints to stderr
    """
    for verse in poem:
        last_word = -1
        penultimate_word = -2
        lim = 2

        if len(verse["words"][-1]["syllables"]) == 0:
            last_word = -2
            penultimate_word = -3
            lim = 3
            msg = f"WARNING: No syllables for the last word: {repr(verse['text'])}"
            if warnings is not None:
                warnings.append(msg)
            else:
                print(msg, file=sys.stderr)

        if len(verse["words"][last_word]["syllables"]) >= 2:  # multi-syllable word
            verse["words"][last_word]["syllables"][-2]["rhyme_from"] = 'v'
            verse["words"][last_word]["syllables"][-1]["rhyme_from"] = 'c'
        elif len(verse["words"]) >= lim and verse["words"][penultimate_word]["vec"] and (verse["words"][penultimate_word]["vec"]["prep"][0] == 1 or verse["words"][last_word]["vec"]["content"][0] == 0):
            verse["words"][penultimate_word]["syllables"][-1]["rhyme_from"] = 'v'
            verse["words"][last_word]["syllables"][-1]["rhyme_from"] = 'c'
        elif verse["words"][last_word]["syllables"][-1]["ph_end_consonants"]:
            verse["words"][last_word]["syllables"][-1]["rhyme_from"] = 'v'
        else:
            if verse["words"][last_word]["syllables"][-1]['ph_consonants']:
                verse["words"][last_word]["syllables"][-1]["rhyme_from"] = 'c'
            else:
                verse["words"][last_word]["syllables"][-1]["rhyme_from"] = 'v'


def get_rhyming_part(syllables):
    """Extract the rhyming part from syllables."""
    r_end = ""
    for i, syllable in enumerate(syllables):
        if syllable['rhyme_from'] == 'c':
            r_end += (syllable['ort_consonants'][-1] if i == 0 else syllable['ort_consonants']) + syllable['ort_vowels'] + syllable['ort_end_consonants']
        elif syllable['rhyme_from'] == 'v':
            r_end += syllable['ort_vowels'] + syllable['ort_end_consonants']
        elif syllable['rhyme_from'] == 'ec':
            r_end += syllable['end_consonants'][-1] if i == 0 else syllable['end_consonants']
        else:
            raise ValueError(f"Invalid rhyme_from value {syllable['rhyme_from']}")
    return r_end


def select_metre(metres):
    """Select the dominant metre from a list."""
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
