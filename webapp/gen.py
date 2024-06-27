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

def _generate(poet_start,
        stop_strings=None,
        temperature=1,
        force_words_ids=None):

    """
    
    
    stop_strings(`str or List[str]`, *optional*):
            A string or a list of strings that should terminate generation if the model outputs them.

    force_words_ids(`List[List[int]]` or `List[List[List[int]]]`, *optional*):
            List of token ids that must be generated. If given a `List[List[int]]`, this is treated as a simple list of
            words that must be included, the opposite to `bad_words_ids`. If given `List[List[List[int]]]`, this
            triggers a [disjunctive constraint](https://github.com/huggingface/transformers/issues/14081), where one
            can allow different forms of each word.


    """


    # tokenize input
    tokenized_poet_start = tokenizer.encode(poet_start, return_tensors='pt')

    # generated a continuation to it
    out = model.generate(
            tokenized_poet_start, 
            max_length=256,
            do_sample=True,
            # top_p=0.7,
            top_k=50,
            # no_repeat_ngram_size=2,
            pad_token_id= tokenizer.pad_token_id,
            eos_token_id = tokenizer.eos_token_id,
            stop_strings=stop_strings,
            temperature=temperature,
            force_words_ids=force_words_ids,
            )

    # Decode Poet
    result = tokenizer.decode(out[0], skip_special_tokens=True)
    cont_length = len(tokenized_poet_start[0])
    continuation = tokenizer.decode(out[0][cont_length:], skip_special_tokens=True)

    # tuple of: (full text, only the generated continuation)
    return result, continuation

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

RHYME_SCHEMES = {
    4: ['ABAB', 'XXXX', 'XAXA', 'AAXX', 'AABB', 'ABBA'],
    6: ['AABBCC', 'XXXXXX', 'ABABXX', 'ABABCC'],
    }

def generuj(rhyme_scheme='AABB', metre='J', verses_count=0, syllables_count=0,
        firstword='', firstline='', year=1900):

    if verses_count not in (4, 6):
        verses_count = random.choice([4, 6])

    # TODO this now also allows thing the model cannot generate
    if not re.match(r'^[A-Z]+$', rhyme_scheme):
        rhyme_scheme = random.choice(RHYME_SCHEMES[verses_count])

    # this is probably not needed here unless verses_count is used for something
    verses_count = len(rhyme_scheme)

    if not metre:
        metre = random.choice(['J', 'T', 'D'])

    if syllables_count not in range(1,20):
        syllables_count = random.choice(range(6, 13))

    poet_start = f'# {rhyme_scheme} # {year}\n{metre} # {syllables_count} #'
    if firstline:
        # TODO format:
        # D # 11 # eště # po letech v polích jsem ohlížel se ještě,
        poet_start += firstline + '\n'
    elif firstword:
        # TODO format:
        # D # 11 # eště # po letech v polích jsem ohlížel se ještě,
        poet_start += firstword

    result, _ = _generate(poet_start)
    result = result.split('\n')

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
