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

STRESS_NORM = {
    'R1': '10',
    'RM': '1m',
    'R0': '10',
    'R': '0',
    'nm': '10',
    'n': '0',
    'm': '0',
    'M': '1',
    'N': '1',
}

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
def get_rhyme_letter(rhyme, nonrhyming=NBSP):
    if rhyme == 0:
        return nonrhyming
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

def get_reduplicant_type(words):
    # TODO format conversion, remove later
    syllables = []
    for word in words:
        for syllable in word["syllables"]:
            syllables.append(syllable)
    if len(syllables) == 0 or not syllables[-1].get("rhyme_from", ""):
        # No syllable, no rhyme
        return '0'
    elif len(syllables) >= 2 and syllables[-2].get("rhyme_from", ""):
        # Penultimate (and necessarily ultimate)  syllable rhymes
        return '2'
    else:
        rhyme_from = syllables[-1]["rhyme_from"]
        if rhyme_from == 'c':
            return '1o'
        else:
            assert rhyme_from == 'v'
            return '1c'

def construct_syllable_parts(syllable, previous_syllable):
    result = []
    # consonants before
    if syllable["ort_consonants"]:
        part = {}
        part['text'] = syllable["ort_consonants"].replace('_', NBSP)
        part['classes'] = []
        part['classes'].append('syllpart')
        part['classes'].append('ort_consonants')
        # position and stress
        if syllable["ort_vowels"]:
            # vowels follow so mark in standard way
            part['classes'].append('beforeposition' +
                    syllable["position"])
            part['classes'].append('beforestress' +
                    syllable["stress"])
            # TODO maybe mark prev stress only if
            # there is no afterstresws or something
            # like that
            prev_position = 'W'
            prev_stress = '0'
            if not previous_syllable["after"]:
                prev_position = previous_syllable["position"]
                prev_stress = previous_syllable["stress"]
            part['classes'].append('afterposition' +
                prev_position)
            part['classes'].append('afterstress' +
                prev_stress)
        else:
            # no vowels, so we need to mark stress on
            # the consonants already
            part['classes'].append('position' +
                    syllable["position"])
            part['classes'].append('stress' +
                    syllable["stress"])
        result.append(part)
    # vowel
    if syllable["ort_vowels"]:
        part = {}
        part['text'] = syllable["ort_vowels"]
        part['classes'] = []
        part['classes'].append('syllpart')
        part['classes'].append('ort_vowels')
        # position and stress
        part['classes'].append('position' +
                syllable["position"])
        part['classes'].append('stress' +
                syllable["stress"])
        result.append(part)
    # consonants after (= end of verse)
    if syllable["ort_end_consonants"]:
        part = {}
        part['text'] = syllable["ort_end_consonants"]
        part['classes'] = []
        part['classes'].append('syllpart')
        part['classes'].append('ort_end_consonants')
        # position and stress
        part['classes'].append('afterposition' +
                syllable["position"])
        part['classes'].append('afterstress' +
                syllable["stress"])
        result.append(part)
    return result

def mark_rhyming(parts, span):
    """
    parts = list of parts, part = dict of text and classes
    span = a (all), v (from vowel), c (from last consonant preceding vowel)
    """
    part0 = None
    part1 = None
    for part in parts:
        if "ort_consonants" in part["classes"]:
            # initial consonant cluster
            if span == 'a':
                # everything is rhyming
                part['classes'].append('rhyming')
            elif span == 'c':
                # only last consonant is rhyming
                # need to split the part into two
                part0 = {'classes': []}
                part1 = {'classes': []}
                # text
                if part['text'].endswith('ch'):
                    part0['text'] = part['text'][:-2]
                    part1['text'] = part['text'][-2:]
                else:
                    part0['text'] = part['text'][:-1]
                    part1['text'] = part['text'][-1:]
                # mark classes
                for classname in part['classes']:
                    if classname in ['syllpart', 'ort_consonants']:
                        part0['classes'].append(classname)
                        part1['classes'].append(classname)
                    elif classname.startswith('after'):
                        part0['classes'].append(classname)
                    else:
                        # before, position, stress
                        part1['classes'].append(classname)
                part1['classes'].append('rhyming')
            # else 'v': initial consonant cluster does not rhyme
        else:
            # vowels and end consonants are always rhyming
            part['classes'].append('rhyming')
    if part0 and part1:
        parts.insert(0, part0)
        parts[1] = part1
    

def filename_if_exists(filename):
    if os.path.isfile(filename):
        return filename
    else:
        return None

def contents_if_exists(filename):
    if os.path.isfile(filename):
        with open(filename) as infile:
            return infile.read()
    else:
        return None

def ensure_qr_code(poemid):
    filename = f'static/qrcodes/{poemid}.png'
    if not os.path.isfile(filename):
        import qrcode
        base_url = 'https://quest.ms.mff.cuni.cz/edupo/show?poemid='
        url = f'{base_url}{poemid}'
        img = qrcode.make(url)
        img.save(filename)

def show(data, syllformat=False):
    data = defaultdict(str, data)
    data['json'] = json.dumps(data, indent=4, ensure_ascii=False)
    
    if data['id']:
        data['imgfile'] = filename_if_exists(
                f"static/genimg/{data['id']}.png")
        data['imgtitle'] = contents_if_exists(
                f"static/genimg/{data['id']}.txt")
        data['ttsfile'] = filename_if_exists(
                f"static/gentts/{data['id']}.mp3")
        data['motives'] = contents_if_exists(
                f"static/genmotives/{data['id']}.txt")
        ensure_qr_code(data['id'])

    if 'body' in data:
        # convert verses into a simpler format for displaying
        data['stanzas'] = []
        data['present_metres'] = set()
        prev_stanza_id = 0
        # list of lines (empty = empty line)
        plaintext = list()
        for stanza in data['body']:
            verses = []
            for verse in stanza:
                rhyme = get_rhyme(verse)
                metre, metre_index = get_metre(verse)
                data['present_metres'].add(metre)
                syllables = []
                if syllformat:
                    # Reduplicant
                    if "reduplicant_type" in verse:
                        reduplicant_type = verse["reduplicant_type"]
                    else:
                        # TODO remove this once the format is refactored
                        reduplicant_type = get_reduplicant_type(verse["words"])
                        # TODO default:
                        # reduplicant_type = '0'
                    
                    # stress and metre
                    swv = verse["metre"][metre_index][metre]["pattern"]
                    stress = verse["sections"]
                    pointer = 0
                    syllable_count = sum((len(word["syllables"]) for word in verse["words"]))
                    assert len(swv) == len(stress)
                    if syllable_count != len(swv):
                        logging.warning(
                            f'Syllable count mismatch: {len(swv)} annotated, {syllable_count} found in poem {data["id"]} verse {verse["text"]}')
                        swv = ' ' * syllable_count
                        stress = ' ' * syllable_count
                    for key, value in STRESS_NORM.items():
                        stress = stress.replace(key, value)
                    swv = swv.replace('V', 'W')
    
                    # initialize with empty initial syllable so that we can easily
                    # check against prev syllable and also so that we can add "after"
                    # to it
                    syllables = [{
                        "parts": [],
                        "position": "W",
                        "stress": "0",
                        "after": ""}]
                    for word in verse["words"]:
                        if "punct_before" in word:
                            syllables[-1]["after"] += word["punct_before"]
                        # add all syllables
                        for syllable in word["syllables"]:
                            if 'stress' not in syllable:
                                syllable['position'] = swv[pointer]
                                syllable['stress'] = stress[pointer]
                            parts = construct_syllable_parts(syllable, syllables[-1])
                            syllables.append({
                                "parts": parts,
                                "position": syllable['position'],
                                "stress": syllable['stress'],
                                "after": ""})
                            pointer += 1
                        # mark end of word
                        if "punct" in word:
                            syllables[-1]["after"] += word["punct"]
                        if not syllables[-1]["after"].endswith(NBSP):
                            syllables[-1]["after"] += NBSP
            
                    if reduplicant_type == '2':
                        mark_rhyming(syllables[-2]['parts'], 'v')
                        mark_rhyming(syllables[-1]['parts'], 'a')
                    elif reduplicant_type == '1c':
                        mark_rhyming(syllables[-1]['parts'], 'v')
                    elif reduplicant_type == '1o':
                        mark_rhyming(syllables[-1]['parts'], 'c')
    
                if prev_stanza_id != verse.get("stanza", 0):
                    plaintext.append('')
                    prev_stanza_id = verse.get("stanza", 0)
                plaintext.append(verse["text"])
                
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
                    'narrators_gender': verse.get('narrators_gender', ''),
                    })
    
            plaintext.append('')
            data['stanzas'].append({
                'verses': verses,
                })
                
            # TODO možná restartovat číslování rýmu po každé sloce
            # (ale někdy jde rýmování napříč slokama)
            
        # listify set because JSON cannot serialize sets
        data['present_metres'] = list(data['present_metres'])
        
        data['plaintext'] = '\n'.join(plaintext)
    
    return data

# Reads in file
def show_file(poemid = '78468', path='static/poemfiles'):

    if poemid.endswith('.json'):
        filename = poemid
    else:
        filename = poemid + '.json'

    with open(f'{path}/{filename}') as infile:
        j = json.load(infile)

    if type(j) == dict:
        # new format
        data = j
        if not 'id' in data:
            data['id'] = poemid
        return show(data, True)
    
    elif type(j) == list:
        # old format

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
    
    else:
        assert False, f"Invalid type of root JSON element: {type(j)}"

if __name__=="__main__":
    filename = sys.argv[1]
    data = show_file(filename, path='.')
    html = render_template('show_poem_html.html', **data)
    print(html)
     
