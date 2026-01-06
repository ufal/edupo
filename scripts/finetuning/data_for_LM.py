"""
Data formatter for Language Models - Poem annotation tool

Supports multiple output format versions:
  - Format V1: Uses <reduplicant> tags with each verse's rhyming part
  - Format V2: Uses <rhyme_with> tags referencing the rhyming part from previous verses

Usage:
  python data_for_LM.py > output.jsonl                        # Generate v2 format (default, JSON wrapped)
  python data_for_LM.py --format-version 1 > output.jsonl     # Generate v1 format
  python data_for_LM.py --max-poems 100 > test.jsonl          # Process only 100 poems (faster)
  python data_for_LM.py --no-json > output.txt                # Output with tags but no JSON wrapping
  python data_for_LM.py --plaintext > output.txt              # Generate plaintext only (no tags)
"""

import argparse
import sqlite3
import json
from collections import defaultdict

import sys
sys.path.append("edupo/kveta")
sys.path.append("edupo/scripts/diphthongs")
import kveta
from kveta import Kveta



def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def add_rhyme_annotation(poem):
    for verse in poem:
        #print(verse['text'], file=sys.stderr)
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

# Formatter classes for different format versions
class PoemFormatter:
    """Base class for poem formatters"""

    def format_version_tag(self):
        """Returns the format version tag (e.g., '<format-v-1/>')"""
        raise NotImplementedError

    def format_verse(self, verse, rhyming, stanza, verse_index):
        """Formats a single verse with metadata"""
        raise NotImplementedError


class FormatV1(PoemFormatter):
    """Format V1: Uses <reduplicant> tags with current verse's rhyming part"""

    def format_version_tag(self):
        return "<format-v-1/>"

    def format_verse(self, verse, rhyming, stanza=None, verse_index=None):
        metre = select_metre([list(v)[0] for v in verse['metre']])
        syllables = len(verse['sections'])
        if rhyming:
            rhyme_end = get_rhyming_part(sum([[s for s in w['syllables'] if 'rhyme_from' in s] for w in verse['words']],[])).lower()
        else:
            rhyme_end = 'NON'

        return '<metre>' + metre + '</metre><syllables>' + str(syllables) + '</syllables><reduplicant>' + rhyme_end + "</reduplicant>" + verse['text']


class FormatV2(PoemFormatter):
    """Format V2: Uses <rhyme_with> tags referencing previous verse with same rhyme"""

    def format_version_tag(self):
        return "<format-v-2/>"

    def format_verse(self, verse, rhyming, stanza, verse_index):
        metre = select_metre([list(v)[0] for v in verse['metre']])
        syllables = len(verse['sections'])

        if rhyming and verse['rhyme'] is not None:
            # Find the reduplicant from the previous verse with matching rhyme number
            rhyme_with_text = self._get_rhyme_with(stanza, verse_index, verse['rhyme'])
        else:
            rhyme_with_text = 'NON'

        return '<metre>' + metre + '</metre><syllables>' + str(syllables) + '</syllables><rhyme_with>' + rhyme_with_text + "</rhyme_with>" + verse['text']

    def _get_rhyme_with(self, stanza, current_index, rhyme_num):
        """Find reduplicant from previous verse with same rhyme number"""
        for i in range(current_index):
            if stanza[i]['rhyme'] == rhyme_num:
                # Extract reduplicant from this verse
                syllables_with_rhyme = sum([[s for s in w['syllables'] if 'rhyme_from' in s] for w in stanza[i]['words']], [])
                return get_rhyming_part(syllables_with_rhyme).lower()
        # First occurrence of this rhyme - no previous verse to rhyme with
        return 'NON'

def poem_header(poem, formatter):
    #TODO truecasovat názvy v datech
    header = "<poem>\n"
    header += formatter.format_version_tag() + "\n"
    header += "<rhyme_schemes/>\n"
    header += f"<author>{poem['author']}</author>\n" # TODO randomizovat formát "příjmení, jméno" nebo "jméno příjmení"
    # TODO přidat tag sbírka
    header += f"<title>{poem['title']}</title>\n"
    header += f"<year>{poem['year']}</year>\n"
    if poem['schemes']['form'] is not None:
        header += f"<form>{poem['schemes']['form']}</form>\n"
    header += f"<stanzas>{len(poem['body'])}</stanzas>\n"
    # TODO počet slok
    return header

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
    # TODO zvlášť délka a zvlášť schéma
    return '<new_stanza/>\n' + f'<rhyme_scheme length="{len(scheme)}">' + ' '.join(scheme) + "</rhyme_scheme>\n", len(renum) > 0

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
    syllables = len(verse['sections'])
    if rhyming:
        rhyme_end = get_rhyming_part(sum([[s for s in w['syllables'] if 'rhyme_from' in s] for w in verse['words']],[])).lower()
    else:
        rhyme_end = 'NON'
 
    #return verse['stress'] + ' ' + metre + ' # ' + str(syllables) + ' # ' + rhyme_end + " # " + verse['text'] + " " + str(verse['words'][-1]['vec']) + verse['words'][-1]['morph']
    return '<metre>' + metre + '</metre><syllables>' + str(syllables) + '</syllables><reduplicant>' + rhyme_end + "</reduplicant>" + verse['text']

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


def main(plaintext=False, format_version=2, max_poems=None, no_json=False):

    # Create the appropriate formatter
    formatters = {
        1: FormatV1(),
        2: FormatV2(),
    }
    formatter = formatters.get(format_version)
    if formatter is None:
        raise ValueError(f"Unknown format version: {format_version}")

    sqlite3.register_converter("json", json.loads)
    with sqlite3.connect("../../data/db_s_motivama.db", detect_types=sqlite3.PARSE_DECLTYPES) as db:
        db.row_factory = dict_factory
        # TODO option to include duplicates
        query = "SELECT poems.id, poems.author, poems.title, body, year, poems.schemes FROM poems JOIN books on poems.book_id = books.id WHERE poems.duplicate IS NULL"
        if max_poems is not None:
            query += f" LIMIT {max_poems}"
        query += ";"
        poems = db.execute(query).fetchall()
        print(f"Loaded {len(poems)} poems.", file=sys.stderr)

    #error_ids = []
    #error_string = ""

    for p in poems:
        print(f"Processing {p['id']} {p['author']}: {p['title']} ({p['year']})", file=sys.stderr)
        try:            
            #for s in p['body']:
            #    print(s)
            #   for l in s:
            #       l['stress'] = l['sections']
            #try:
            if not plaintext:
                kv = Kveta('')
                kv.read_ccv(p['body'])
                kv.phoebe2cft()
                kv.syllables()
                #print(p['id'], p['duplicate_tm'])
                #print(p['id'], file=sys.stderr)
                kv.line2vec()
                add_rhyme_annotation(kv.poem_)

                p['body'] = separate_stanzas(kv.poem_)
            else:
                p['body'] = separate_stanzas(p['body'])
            
            #except Exception as e:
            #    error_string += f"Error processing {p['id']} {p['author']}: {p['title']} ({p['year']})" + '\n'
            #    error_string += str(e) + '\n'
            #    error_ids.append(p['id'])
            #    continue

            if plaintext:
                for s in p['body']:
                    print('\n'.join(verse['text'] for verse in s))
                    print()
            else:
                output = ""
                output += poem_header(p, formatter)
                for s in p['body']:
                    output += '\n'
                    s_header, rhyming = strophe_header(s)
                    output += s_header
                    output += '\n'.join([formatter.format_verse(verse, rhyming, s, idx) for idx, verse in enumerate(s)])
                output += '\n</poem>'
                if no_json:
                    print(output)
                else:
                    print(json.dumps({'text': output}, ensure_ascii=False))
        except Exception as e:
            print(f"ERROR: Error processing {p['id']} {p['author']}: {p['title']} ({p['year']})", file=sys.stderr)
            print(str(e), file=sys.stderr)
            continue

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--plaintext", action="store_true",
                        help="Output plaintext only (no formatting)")
    parser.add_argument("--format-version", type=int, default=2, choices=[1, 2],
                        help="Output format version (default: 2)")
    parser.add_argument("--max-poems", type=int, default=None,
                        help="Maximum number of poems to process (default: all)")
    parser.add_argument("--no-json", action="store_true",
                        help="Output formatted text without JSON wrapping")

    args = parser.parse_args()

    main(plaintext=args.plaintext, format_version=args.format_version, max_poems=args.max_poems, no_json=args.no_json)