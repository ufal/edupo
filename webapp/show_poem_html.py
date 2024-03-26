#!/usr/bin/env python3
#coding: utf-8

import sys

import logging
logging.basicConfig(
    format='%(asctime)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO)

import json

from string import Template

# Reads in file

filename = sys.argv[1]

with open(filename) as infile:
    j = json.load(infile)

with open('html/show_poem_html.html') as infile:
    html = Template(infile.read())

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

verses = []
for stanza in j[0]["body"]:
    for verse in stanza:
        verses.append(verse["text"])
    verses.append('')
replacements['text'] = '\n'.join(verses)

print(html.substitute(replacements))

