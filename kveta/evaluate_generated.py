#!/usr/bin/env python3
#coding: utf-8

import sys
sys.path.append("../backend")
import parser
import parsy
sys.path.append("../kveta")
from kveta import okvetuj
from get_measures import get_measures
from functools import reduce

poems = []
current_poem = ""
separator = False
with open(sys.argv[1], 'r') as file:
    for line in file:
        if line.startswith("================================================================================") or line.startswith("temperature = "):
            separator = True
            if current_poem:
                poems.append(current_poem)
                current_poem = ""
        else:
            current_poem += line
    if current_poem:
        poems.append(current_poem)

with open('../backend/prompt_templates/tm1.txt', 'r') as f:
     template_tm = parser.Template(f.read())

for i, poem in enumerate(poems):
    poem = poem.split('<|end_of_text|>')[0]
    print('Processing poem', i, file=sys.stderr)

    try:
        parsed = (parsy.string('<|begin_of_text|>').optional() >> template_tm.poem_parser()).parse(poem + '\n\n') # TODO fix hack with \n\n
        author_name = parsed.get('author_name')
        title = parsed.get('poem_title')
        verses = reduce(lambda x, y: x + [''] + y, [[v['line'] for v in s['verses']] for s in parsed['stanzas']])
    except parsy.ParseError as e:
        print("EXCEPTION Nepodařený parsing básně:" + str(e), file=sys.stderr)
        continue

    try:
        results = get_measures("\n".join(verses) + "\n")
        
    except:
        print('ERROR while processing file:', i, file=sys.stderr)
        raise
    print(i, results['unknown_words'], results['rhyming'], results['metre_consistency'], results['syllable_count_entropy'], results['rhyming_consistency'], sep="\t")

