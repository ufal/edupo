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

tokenizer = AutoTokenizer.from_pretrained("jinymusim/gpt-czech-poet")
model = AutoModelForCausalLM.from_pretrained("jinymusim/gpt-czech-poet")

metra = {
    'J': 'jamb',
    'T': 'trochej',
        }

while True:

    # Input Poet Start
    poet_start = input('Zadej rýmové schéma, např. AABB nebo ABCABC: ')
    poet_start = poet_start.strip().upper()
    if not poet_start:
        poet_start = 'AABB'

    # tokenize input
    tokenized_poet_start = tokenizer.encode(poet_start, return_tensors='pt')

    # generated a continuation to it
    out = model.generate(
            tokenized_poet_start, 
            max_length=256,
            num_beams=8,
            no_repeat_ngram_size=2,
            early_stopping=True,
            pad_token_id= tokenizer.pad_token_id,
            eos_token_id = tokenizer.eos_token_id
            )

    # Decode Poet
    decoded_cont = tokenizer.decode(out[0], skip_special_tokens=True)

    result = decoded_cont.split('\n')
    header = result[0]
    try:
        schema, year, meter = header.split(' # ')
        if meter in metra:
            meter = metra[meter]
    except:
        schema = poet_start
        year = '?'
        meter = '?'
    poem = result[1:]

    print()
    print(f'''Zde je vygenerovaná báseň s rýmovým schématem {schema}, používající metrum typu {meter}, ve stylu roku {year}:''')
    print()
    for line in poem:
        try:
            cleanline = line.split('#')[1].strip()
        except:
            cleanline = line
        print(cleanline)

    print()


