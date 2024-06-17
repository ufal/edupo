#!/usr/bin/env python3
#coding: utf-8

import sys

import logging
logging.basicConfig(
    format='%(asctime)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO)

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import random
import re

tokenizer = AutoTokenizer.from_pretrained("jinymusim/gpt-czech-poet")
model = AutoModelForCausalLM.from_pretrained("jinymusim/gpt-czech-poet")

END_PUNCT = set(['.', '?', '!'])
def clean(verses):
    result = []
    last = '.'
    for verse in verses:
        if verse:
            if last in END_PUNCT:
                verse = verse.capitalize()
            last = verse[-1]
            result.append(verse)
    # should not end with ,
    if result[-1][-1] == ',':
        result[-1] = result[-1][:-1] + '.'

    return result

def generuj(rhyme_scheme='AABB', metre='J', firstword='', firstline='', year=1900):

    # TODO this now also allows thing the model cannot generate
    if not re.match(r'^[A-Z]+$', rhyme_scheme):
        rhyme_scheme = random.choice(['ABAB', 'XXXX', 'XAXA', 'XXXXXX', 'AABB', 'ABBA', 'AABBCC', 'AAXX', 'ABABXX', 'ABABCC'])

    if not metre:
        metre = random.choice(['J', 'T', 'D'])

    poet_start = f'# {rhyme_scheme} # {year}\n{metre} #'
    if firstline:
        # TODO format:
        # D # 11 # eště # po letech v polích jsem ohlížel se ještě,
        poet_start += firstline + '\n'
    elif firstword:
        # TODO format:
        # D # 11 # eště # po letech v polích jsem ohlížel se ještě,
        poet_start += firstword

    # tokenize input
    tokenized_poet_start = tokenizer.encode(poet_start, return_tensors='pt')

    # generated a continuation to it
    out = model.generate(
            tokenized_poet_start, 
            max_length=256,
            do_sample=True,
            # top_p=0.7,
            top_k=50,
            temperature=1,
            # no_repeat_ngram_size=2,
            pad_token_id= tokenizer.pad_token_id,
            eos_token_id = tokenizer.eos_token_id
            )

    # Decode Poet
    decoded_cont = tokenizer.decode(out[0], skip_special_tokens=True)

    result = decoded_cont.split('\n')
    header = result[0]
    try:
        _, schema, year = header.split('#')
    except:
        schema = rhyme_scheme
        year = '?'
    poem = result[1:]

    for line in poem:
        try:
            meter, syls, end, verse = line.split('#')
        except:
            verse = line
        result.append(verse.strip())
    
    # TODO výhledově možná rovnou vracet v JSON formátu
    clean_verses = clean(result[-len(rhyme_scheme)-1:])
    return result, clean_verses

if __name__=="__main__":
    try:
        rhyme_scheme = sys.argv[1]
    except:
        rhyme_scheme = 'AABB'

    verses = generuj(rhyme_scheme)
    print(*verses, sep='\n')
