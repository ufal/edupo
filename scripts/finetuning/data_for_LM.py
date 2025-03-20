import sqlite3
import json
from collections import defaultdict

import sys
sys.path.append("edupo/kveta")
sys.path.append("edupo/scripts/diphthongs")
import kveta
from kveta import Kveta

sqlite3.register_converter("json", json.loads)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def add_rhyme_annotation(poem):
    for verse in poem:
        print(verse['text'], file=sys.stderr)
        #print(verse['words'], file=sys.stderr)
        last_word = -1
        penultimate_word = -2
        lim = 2

        if len(verse["words"][-1]["syllables"]) == 0:
            last_word = -2
            penultimate_word = -3
            lim = 3
            print("WARNING: No syllables for the last word: " + repr(verse['text']), file=sys.stderr)
    
        if len(verse["words"][last_word]["syllables"]) >= 2: # víceslabičné slovo
            verse["words"][last_word]["syllables"][-2]["rhyme_from"] = 'v'
            verse["words"][last_word]["syllables"][-1]["rhyme_from"] = 'c'
        elif len(verse["words"]) >= lim and verse["words"][penultimate_word]["vec"] and (verse["words"][penultimate_word]["vec"]["prep"][0] == 1 or verse["words"][last_word]["vec"]["content"][0] == 0): # jednoslabičné slovo za slabičkou předložkou nebo nepřízvučný monosylabon
            verse["words"][penultimate_word]["syllables"][-1]["rhyme_from"] = 'v'
            verse["words"][last_word]["syllables"][-1]["rhyme_from"] = 'c'
        elif verse["words"][last_word]["syllables"][-1]["ph_end_consonants"]: # jednoslabičné slovo bez předložky končící souhláskou
            verse["words"][last_word]["syllables"][-1]["rhyme_from"] = 'v'
        else:                                                           # jednoslabičné slovo bez předložky končící samohláskou
            if verse["words"][last_word]["syllables"][-1]['ph_consonants']:
                verse["words"][last_word]["syllables"][-1]["rhyme_from"] = 'c'
            else:
                verse["words"][last_word]["syllables"][-1]["rhyme_from"] = 'v'


METRE_PRIORITY = defaultdict(int)                                                                                                                                                             
METRE_PRIORITY['T'] = 5                                                                                                                                                                       
METRE_PRIORITY['J'] = 4                                                                                                                                                                       
METRE_PRIORITY['D'] = 3                                                                                                                                                                       
METRE_PRIORITY['A'] = 2                                                                                                                                                                       
METRE_PRIORITY['N'] = -1

# TODO: duplikáty

def poem_header(poem):
    #TODO truecasovat název?
    return f"{poem['author']}: {poem['title']} ({poem['year']})"

def strophe_header(strophe):
    # TODO: zatím po slokách, chceme to pro celou báseň?
    abeceda = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    scheme_numeric = [v['rhyme'] for v in strophe]
    for n in scheme_numeric:
        assert n is None or 0 < n, f"Invalid rhyme number {n}"
    renum = {}
    scheme = []
    for n in scheme_numeric:
        if n is None:
            scheme.append('x')
            continue
        if n not in renum:
            renum[n] = len(renum)
        scheme.append(abeceda[renum[n] % len(abeceda)])
    return "# " + ' '.join(scheme) + " #", len(renum) > 0

def get_rhyming_part(syllables):
    r_end = ""
    for i, syllable in enumerate(syllables):
        if syllable['rhyme_from'] == 'c':
            r_end += (syllable['ort_consonants'][-1] if i == 0 else syllable['ort_consonants']) + syllable['ort_vowels'] + syllable['ort_end_consonants']
        elif syllable['rhyme_from'] == 'v':
            r_end += syllable['ort_vowels'] + syllable['ort_end_consonants']
        elif syllable['rhyme_from'] == 'ec':
            r_end += syllable['end_consonants'][-1] if i == 0 else syllable['end_consonants']
        else:
            assert False, f"Invalid rhyme_from value {syllable['rhyme_from']}"
    return r_end

def select_metre(metres):
    return max(metres, key=lambda m: METRE_PRIORITY[m])

def format_verse(verse, rhyming=True, pid=None):
    metre = select_metre([list(v)[0] for v in verse['metre']])
    syllables = len(verse['metre'][0][list(verse['metre'][0])[0]]['pattern'])
    if rhyming:
        rhyme_end = get_rhyming_part(sum([[s for s in w['syllables'] if 'rhyme_from' in s] for w in verse['words']],[])).lower()
    else:
        rhyme_end = 'NON'
 
    #return verse['stress'] + ' ' + metre + ' # ' + str(syllables) + ' # ' + rhyme_end + " # " + verse['text'] + " " + str(verse['words'][-1]['vec']) + verse['words'][-1]['morph']
    return '# ' + metre + ' # ' + str(syllables) + ' # ' + rhyme_end + " # " + verse['text']

def separate_stanzas(poem):
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



with sqlite3.connect("new.db", detect_types=sqlite3.PARSE_DECLTYPES) as db:
    db.row_factory = dict_factory
    poems = db.execute("SELECT poems.id, poems.author, poems.title, body, year FROM poems JOIN books on poems.book_id = books.id;").fetchall()

error_ids = []
error_string = ""

for p in poems[79402:]:
    if p['id'] in [
        4110, # TODO: fix J. S. M. fonetický přepis
        9273, # TODO: vis-a-vis
        20760, # TODO: T...c
        28450, # TODO: druhY
        29099, # TODO: tête à tête
        29111, # TODO: tête à tête
        35556, # TODO: tête à tête
        35557, # TODO: tête à tête
        36453, # TODO: tête à tête
        50826, # TODO: SERVER ERROR
        53455, # TODO: slabikotvorné Ž
        60317, # TODO: vis-a-vis
        65960, # TODO: W se změní v Z
        68782, # TODO: vis-a-vis
        75302, # TODO: RSFSR?
        75704, # ? (pštrosí péro)
        79402, # ? (pštrosí péro)
    ]:
        continue
    for s in p['body']:
        for l in s:
            l['stress'] = l['sections']
    #try:
    kv = Kveta('')
    kv.read_ccv(p['body'])
    kv.phoebe2cft()
    kv.syllables()
    #print(p['id'], p['duplicate_tm'])
    print(p['id'], file=sys.stderr)
    kv.line2vec()
    add_rhyme_annotation(kv.poem_)
    #except Exception as e:
    #    error_string += f"Error processing {p['id']} {p['author']}: {p['title']} ({p['year']})" + '\n'
    #    error_string += str(e) + '\n'
    #    error_ids.append(p['id'])
    #    continue

    p['body'] = separate_stanzas(kv.poem_)

    print('<|begin_of_text|>' + poem_header(p))
    for s in p['body']:
        print()
        s_header, rhyming = strophe_header(s)
        print(s_header)
        print('\n'.join([format_verse(l, rhyming) for l in s]))
        
    print('<|end_of_text|>')

#print(error_string)
#print(error_ids)

def fix_kiel(poem):
    for s in poem:
        if s['text'] == 'jež pýchou severního Kielu.':
            s['words'][-1]['syllables'] = [
                {'ph_consonants': '', 'ph_vowels': '', 'ph_end_consonants': '', 'ort_consonants': '', 'ort_vowels': 'ie', 'ort_end_consonants': '', 'length': 0, 'rhyme_from': 'v'},
                {'ph_consonants': '', 'ph_vowels': '', 'ph_end_consonants': '', 'ort_consonants': 'l', 'ort_vowels': 'u', 'ort_end_consonants': '', 'length': 0, 'rhyme_from': 'c'},
            ]
        elif s['text'] == 'Chopina miluj, jenž jest hudby Baudelairem,':
            s['words'][-1]['syllables'] = [
                {'ph_consonants': '', 'ph_vowels': '', 'ph_end_consonants': '', 'ort_consonants': '', 'ort_vowels': 'ai', 'ort_end_consonants': '', 'length': 0, 'rhyme_from': 'v'},
                {'ph_consonants': '', 'ph_vowels': '', 'ph_end_consonants': '', 'ort_consonants': 'r', 'ort_vowels': 'e', 'ort_end_consonants': 'm', 'length': 0, 'rhyme_from': 'c'},
            ]
        elif s['text'] == 'tatíček náš v Naardenu,':
            s['words'][-1]['syllables'] = [
                {'ph_consonants': '', 'ph_vowels': '', 'ph_end_consonants': '', 'ort_consonants': '', 'ort_vowels': 'e', 'ort_end_consonants': '', 'length': 0, 'rhyme_from': 'v'},
                {'ph_consonants': '', 'ph_vowels': '', 'ph_end_consonants': '', 'ort_consonants': 'n', 'ort_vowels': 'u', 'ort_end_consonants': '', 'length': 0, 'rhyme_from': 'c'},
            ]
        elif s['text'] == 'v hranolu se tvého spleenu –':
            s['words'][-1]['syllables'] = [
                {'ph_consonants': '', 'ph_vowels': '', 'ph_end_consonants': '', 'ort_consonants': '', 'ort_vowels': 'ee', 'ort_end_consonants': '', 'length': 0, 'rhyme_from': 'v'},
                {'ph_consonants': '', 'ph_vowels': '', 'ph_end_consonants': '', 'ort_consonants': 'n', 'ort_vowels': 'u', 'ort_end_consonants': '', 'length': 0, 'rhyme_from': 'c'},
            ]
        elif s['text'] == 'ti plam a tryská žár v můj spleen.':
            s['words'][-1]['syllables'] = [
                {'ph_consonants': '', 'ph_vowels': '', 'ph_end_consonants': 'n', 'ort_consonants': 'spl', 'ort_vowels': 'ee', 'ort_end_consonants': 'n', 'length': 0, 'rhyme_from': 'v'},
            ]
        elif s['text'] == 'žár démonický Beethovena':
            s['words'][-1]['syllables'] = [
                {'ph_consonants': '', 'ph_vowels': '', 'ph_end_consonants': '', 'ort_consonants': '', 'ort_vowels': 'e', 'ort_end_consonants': '', 'length': 0, 'rhyme_from': 'v'},
                {'ph_consonants': '', 'ph_vowels': '', 'ph_end_consonants': '', 'ort_consonants': 'n', 'ort_vowels': 'a', 'ort_end_consonants': '', 'length': 0, 'rhyme_from': 'c'},
            ]
        elif s['text'] == 'a bude nade vším, jak z rytby Dürera,':
            s['words'][-1]['syllables'] = [
                {'ph_consonants': '', 'ph_vowels': '', 'ph_end_consonants': '', 'ort_consonants': '', 'ort_vowels': 'e', 'ort_end_consonants': '', 'length': 0, 'rhyme_from': 'v'},
                {'ph_consonants': '', 'ph_vowels': '', 'ph_end_consonants': '', 'ort_consonants': 'r', 'ort_vowels': 'a', 'ort_end_consonants': '', 'length': 0, 'rhyme_from': 'c'},
            ]
