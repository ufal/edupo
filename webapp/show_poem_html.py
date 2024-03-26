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

# Reads in file

filename = sys.argv[1]

with open(filename) as infile:
    j = json.load(infile)

with open('html/show_poem_html.html') as infile:
    html = Template(infile.read())
with open('html/stanza.html') as infile:
    stanza_html = Template(infile.read())
with open('html/verse.html') as infile:
    verse_html = Template(infile.read())

replacements = {}

replacements['p_title'] = j[0]["biblio"]["p_title"]
replacements['p_author'] = j[0]["p_author"]["name"]
replacements['schools'] = ', '.join(j[0]["p_schools"])
replacements['born'] = j[0]["p_author"]["born"]
replacements['died'] = j[0]["p_author"]["died"]
replacements['b_title'] = j[0]["biblio"]["b_title"]
replacements['year'] = j[0]["biblio"]["year"]
replacements['filename'] = filename
replacements[''] = ''
replacements[''] = ''

# print("SLOKY:", len(j[0]["body"]))

# rhyme is 1-based
# nonrhyming = None, converts to 0
RYM = ' ' + 10*string.ascii_uppercase

stanzas_html = []
for stanza in j[0]["body"]:
    verses_html = []
    for verse in stanza:
        rhyme = 0 if verse["rhyme"] == None else verse["rhyme"]
        verses_html.append(verse_html.substitute(
            text=verse["text"],
            rhyme=rhyme,
            rym=RYM[int(rhyme)],
            ))
    stanzas_html.append(stanza_html.substitute(
        verses='\n'.join(verses_html)
        ))
        
    # TODO možná restartovat číslování rýmu po každé sloce
    # (ale někdy jde rýmování napříč slokama)

replacements['body'] = '\n'.join(stanzas_html)

print(html.substitute(replacements))

