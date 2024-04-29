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
from string import Template

# TODO rewrite using Jinja probably?
# from flask import render_template

# Reads in file

def show_file(filename = '78468.json'):

    with open(filename) as infile:
        j = json.load(infile)

    with open('html/show_poem_html.html') as infile:
        html = Template(infile.read())
    with open('html/stanza.html') as infile:
        stanza_html = Template(infile.read())
    with open('html/verse.html') as infile:
        verse_html = Template(infile.read())

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


    replacements = {}

    replacements['p_title'] = get_j0_key_key(j, "biblio", "p_title")
    replacements['p_author'] = get_j0_key_key(j, "p_author", "name")
    replacements['schools'] = ', '.join(get_j0_key(j, "p_schools", []))
    replacements['born'] = get_j0_key_key(j, "p_author", "born")
    replacements['died'] = get_j0_key_key(j, "p_author", "died")
    replacements['b_title'] = get_j0_key_key(j, "biblio", "b_title")
    replacements['year'] = get_j0_key_key(j, "biblio", "year")
    replacements['filename'] = filename
    replacements[''] = ''
    replacements[''] = ''

    # print("SLOKY:", len(j[0]["body"]))

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

    stanzas_html = []
    for stanza in j[0]["body"]:
        verses_html = []
        for verse in stanza:
            rhyme = get_rhyme(verse)
            metre = get_metre(verse)
            verses_html.append(verse_html.substitute(
                text=verse["text"],
                rhyme=rhyme,
                rym=RYM[int(rhyme)],
                metrum=get_metrum(metre),
                ))
        stanzas_html.append(stanza_html.substitute(
            verses='\n'.join(verses_html)
            ))
            
        # TODO možná restartovat číslování rýmu po každé sloce
        # (ale někdy jde rýmování napříč slokama)

    replacements['body'] = '\n'.join(stanzas_html)
    
    return html.substitute(replacements)


if __name__=="__main__":
    filename = sys.argv[1]
    print(show_file(filename))
     
