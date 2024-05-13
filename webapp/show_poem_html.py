#!/usr/bin/env python3
#coding: utf-8

import sys

import logging
logging.basicConfig(
    format='%(asctime)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO)

import json
import string
from collections import defaultdict

from flask import render_template

# TODO rewrite using Jinja probably?
# from flask import render_template

# rhyme is 1-based
# nonrhyming = None, converts to 0
RYM = ' ' + 10*string.ascii_uppercase

METRUM = {
    'J': "jamb",
    'T': "trochej",
    'D': "daktyl",
        }

def get_metrum(metre):
    if metre in METRUM:
        return METRUM[metre]
    else:
        return f"metrum {metre}"

def get_metre(verse):
    try:
        return list(verse["metre"][0].keys())[0]
    except:
        logging.warning(f"Missing metre in data.")
        return '?'

def get_rhyme(verse):
    try:
        rhyme = 0 if verse["rhyme"] == None else verse["rhyme"]
        int(rhyme)
        return rhyme
    except:
        logging.warning(f"Missing valid rhyme in data.")
        return 0


def show(data, syllformat=False):
    data = defaultdict(str, data)

    data['stanzas'] = []
    for stanza in data['body']:
        verses = []
        for verse in stanza:
            rhyme = get_rhyme(verse)
            metre = get_metre(verse)
            syllables = []
            if syllformat:
                for word in verse["words"]:
                    for syllable in word["syllables"]:
                        syllable["ort_consonants"] = syllable["ort_consonants"].replace('_', ' ')
                        syllables.append(syllable)
                    # mark end of word
                    syllables[-1]["class"] = "endofword"
            verses.append({
                'text': verse["text"],
                'syllables': syllables,
                'rhyme': rhyme,
                'rym': RYM[int(rhyme)],
                'metrum': get_metrum(metre),
                })
        data['stanzas'].append({
            'verses': verses,
            })
            
        # TODO možná restartovat číslování rýmu po každé sloce
        # (ale někdy jde rýmování napříč slokama)

    data["json"] = json.dumps(data, indent=4, ensure_ascii=False)

    return render_template('show_poem_html.html', **data)


# Reads in file
def show_file(filename = '78468.json'):

    with open(filename) as infile:
        j = json.load(infile)

    def get_j0_key(j, key1, default=''):
        try:
            return j[0][key1]
        except:
            logging.warning(f"Missing {key1} in data.")
            return default

    def get_j0_key_key(j, key1, key2, default=''):
        try:
            return j[0][key1][key2]
        except:
            logging.warning(f"Missing {key1} {key2} in data.")
            return default


    data = {}

    data['title'] = get_j0_key_key(j, "biblio", "p_title")
    data['author'] = get_j0_key_key(j, "p_author", "name")
    data['schools'] = ', '.join(get_j0_key(j, "p_schools", []))
    data['born'] = get_j0_key_key(j, "p_author", "born")
    data['died'] = get_j0_key_key(j, "p_author", "died")
    data['b_title'] = get_j0_key_key(j, "biblio", "b_title")
    data['year'] = get_j0_key_key(j, "biblio", "year")
    data['id'] = filename
    data['body'] = j[0]["body"]

    return show(data, True)

if __name__=="__main__":
    filename = sys.argv[1]
    print(show_file(filename))
     
