#!/usr/bin/env python3
#coding: utf-8

import sys
import os
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

METRUM = {
    'J': "jamb",
    'T': "trochej",
    'D': "daktyl",
    'A': "amfibrach",
    'N': "neurčeno",
    'alex': "alexandrín (jamb)",
}

# non breaking space
NBSP = ' '

def get_metrum(metre):
    if metre in METRUM:
        return METRUM[metre]
    else:
        return f"metrum {metre}"

# pokud je pro jeden verš anotováno víc meter,
# zobrazit jen to nejnormálnější metrum

METRE_PRIORITY = defaultdict(int)
METRE_PRIORITY['T'] = 5
METRE_PRIORITY['J'] = 4
METRE_PRIORITY['D'] = 3
METRE_PRIORITY['A'] = 2
METRE_PRIORITY['N'] = -1

def get_metre(verse):
    metre = 'N'
    metre_index = 0
    try:
        for index, metredict in enumerate(verse["metre"]):
            metre_candidate = list(metredict.keys())[0]
            if METRE_PRIORITY[metre_candidate] >= METRE_PRIORITY[metre]:
                metre = metre_candidate
                metre_index = index
    except:
        logging.warning(f"Missing metre in data.")
    return metre, metre_index

def get_rhyme(verse):
    try:
        rhyme = 0 if verse["rhyme"] == None else verse["rhyme"]
        return int(rhyme)
    except:
        logging.warning(f"Missing valid rhyme in data.")
        return 0

# rhyme is 1-based
# nonrhyming = None, converts to 0
def get_rhyme_letter(rhyme):
    if rhyme == 0:
        return NBSP
    else:
        index = (rhyme-1) % 26
        return string.ascii_uppercase[index]

def get_rhyme_subscript(rhyme):
    if rhyme <= 26:
        return ''
    else:
        return (rhyme-1) // 26 + 1

def get_rhyme_class(rhyme):
    if rhyme == 0:
        return 0
    else:
        # modulo 12, 1-based
        return (rhyme-1)%12+1

def show(data, syllformat=False):
    data = defaultdict(str, data)
    data['json'] = json.dumps(data, indent=4, ensure_ascii=False)
    
    if data['id']:
        imgfile = f"static/genimg/{data['id']}.png"
        if os.path.isfile(imgfile):
            data['imgfile'] = imgfile
        ttsfile = f"static/gentts/{data['id']}.mp3"
        if os.path.isfile(ttsfile):
            data['ttsfile'] = ttsfile
    
    # convert verses into a simpler format for displaying
    data['stanzas'] = []
    data['present_metres'] = set()
    for stanza in data['body']:
        verses = []
        for verse in stanza:
            rhyme = get_rhyme(verse)
            metre, metre_index = get_metre(verse)
            data['present_metres'].add(metre)
            syllables = []
            if syllformat:
                for word in verse["words"]:
                    if word["syllables"]:
                        for syllable in word["syllables"]:
                            syllable = syllable.copy()
                            syllable["ort_consonants"] = syllable["ort_consonants"].replace('_', NBSP)
                            syllables.append(syllable)
                        # mark end of word
                        if syllables:
                            syllables[-1]["after"] = ""
                            if "punct" in word:
                                syllables[-1]["after"] += word["punct"]
                            syllables[-1]["after"] += NBSP
                
            verses.append({
                'text': verse["text"],
                'stanza': verse.get("stanza", 0),
                'syllables': syllables,
                # NOTE: classes verseNone and verse1..verse12 harwired in CSS
                'rhymeclass': get_rhyme_class(rhyme),
                'rhymeletter': get_rhyme_letter(rhyme),
                'rhymesubscript': get_rhyme_subscript(rhyme),
                'metre': metre,
                'metrum': get_metrum(metre),
                'rythm': verse["sections"],
                'pattern': verse["metre"][metre_index][metre]['pattern'],
                'foot': verse["metre"][metre_index][metre]['foot'],
                'clause': verse["metre"][metre_index][metre]['clause'],
                })

        data['stanzas'].append({
            'verses': verses,
            })
            
        # TODO možná restartovat číslování rýmu po každé sloce
        # (ale někdy jde rýmování napříč slokama)

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
     
