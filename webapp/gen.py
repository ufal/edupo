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
        temperature=1):

    """
    stop_strings(`str or List[str]`, *optional*):
            A string or a list of strings that should terminate generation if the model outputs them.
            The original implementation did not work for me, so I did my own
            with eos_token_id, but this requires the stop_strings to be full
            tokens (so e.g. ' #' instead of just '#').
    """

    # tokenize input
    tokenized_poet_start = tokenizer.encode(poet_start, return_tensors='pt')

    eos_tokens = [tokenizer.eos_token_id]
    if stop_strings:
        if isinstance(stop_strings, str):
            eos_tokens.append(tokenizer.encode(stop_strings)[0])
        elif isinstance(stop_strings, list):
            for s in stop_strings:
                eos_tokens.append(tokenizer.encode(s)[0])

    # generated a continuation to it
    out = model.generate(
            tokenized_poet_start,
            max_length=256,
            do_sample=True,
            # top_p=0.7,
            top_k=50,
            # no_repeat_ngram_size=2,
            pad_token_id= tokenizer.pad_token_id,
            eos_token_id = eos_tokens,
            temperature=temperature,
            )

    # Decode Poet
    result = tokenizer.decode(out[0], skip_special_tokens=True)
    
    return result

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
        first_words=[], first_line='', year=1900):

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

    poet_start = f'# {rhyme_scheme} # {year}\n'
    # D # 11 # eště # po letech v polích jsem ohlížel se ještě,
    if first_line:
        # !! TODO fix this !!
        ending_hint = first_line[:3]  
        # !! TODO set syllables_count properly !!
        poet_start = f"{poet_start}{metre} # {syllables_count} # {ending_hint} # {first_line}\n"
    elif first_words:
        assert type(first_words) == list, "first_words must be list"
        for word in first_words:
            poet_start = f'{poet_start}{metre} # {syllables_count} #'
            # generate ending hint
            poet_start = _generate(poet_start, stop_strings=' #')
            # force word
            poet_start = f"{poet_start} {word}"
            # generate line
            poet_start = _generate(poet_start, stop_strings='\n')
    else:
        poet_start = f'{poet_start}{metre} # {syllables_count} #'

    raw = _generate(poet_start)
    result = raw.split('\n')

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
    return raw, clean_verses

if __name__=="__main__":
    try:
        rhyme_scheme = sys.argv[1]
    except:
        rhyme_scheme = 'AABB'

    verses = generuj(rhyme_scheme)
    print(*verses, sep='\n')
