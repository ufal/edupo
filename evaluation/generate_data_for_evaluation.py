#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append("../backend")
import parser
import parsy
sys.path.append("../kveta")
from kveta import okvetuj
from get_measures import get_measures
from functools import reduce
import fileinput
import random

with open('../backend/prompt_templates/tm1.txt', 'r') as f:
    template = parser.Template(f.read())

PARSE_ERRORS = 0

def read_poem(lines):
    txt = "".join(lines)
    try:
        parsed = (parsy.string('<|begin_of_text|>').optional()
            >> template.poem_parser()).parse(txt + '\n\n') # TODO fix hack with \n\n
    except parsy.ParseError as e:
        print(e, file=sys.stderr)
        global PARSE_ERRORS
        PARSE_ERRORS += 1
        return ['', '', '', '', '']

    author_name = parsed.get('author_name')
    title = parsed.get('poem_title')
    year = parsed.get('year')
    rhyme_schemes = []

    for s in parsed['stanzas']:
        rhyme_schemes.append(s.get('rhyme_scheme'))

    verses = reduce(lambda x, y: x + [''] + y,
                    [[v['line'] for v in s['verses']] for s in parsed['stanzas']])

    return ['"'+author_name+'"', '"'+title+'"', '"'+year+'"', '"'+"\n".join(rhyme_schemes)+'"', '"'+"\n".join(verses)+'"'] 

with open(sys.argv[1], 'r') as f:
    first_line = f.readline()
    if first_line[0] == "🦥":
        for _ in range(7):
            f.readline()
    lines = [f.readline()]

    selected_indices = []
    for i in range(int(sys.argv[3])):
        selected_indices.append(random.randint(1, int(sys.argv[4])))
    print("Selected indices:", selected_indices, file=sys.stderr)

    counter = 0
    for line in f:
        if "<|begin_of_text|>" in line:
            if counter in selected_indices:
                poem = read_poem(lines)
                print (counter, sys.argv[2], poem[0], poem[1], poem[2], poem[3], poem[4], sep=",")
            lines = [line]
            counter += 1
        else:
            lines.append(line)
    print(f"Parse errors: {PARSE_ERRORS}", file=sys.stderr)
