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

tokenizer = AutoTokenizer.from_pretrained("jinymusim/gpt-czech-poet")
model = AutoModelForCausalLM.from_pretrained("jinymusim/gpt-czech-poet")

def generuj(rhyme_scheme='AABB', metre='J', year=1900):

    if not metre:
        metre = random.choice(['J', 'T', 'D'])

    poet_start = f'# {rhyme_scheme} # {year}\n{metre} #'
    result = []

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
   
    # TODO vracet zvlášť raw data a zvlášť clean výstup
    # TODO výhledově možná rovnou vracet v JSON formátu
    return result

if __name__=="__main__":
    try:
        rhyme_scheme = sys.argv[1]
    except:
        rhyme_scheme = 'AABB'

    verses = generuj(rhyme_scheme)
    print(*verses, sep='\n')
