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

while True:

    # Input Poet Start
    # default_poet_start = "AABB # 1900 # D"
    prompt = '\n'.join([
        'Zadej požadavek ve formátu:',
        'RÝMOVÉ SCHÉMA # ROK VYDÁNÍ # METRUM',
        'například:',
        'AABB # 1900 # D',
        '(stačí zadat i jen některé parametry, chybějící si model vymyslí)'
        '\n'
        ])
    poet_start = input(prompt)
    
    # process input
    poet_start = poet_start.strip()
    tokenized_poet_start = tokenizer.encode(poet_start, return_tensors='pt')

    # generated a continuation to it
    # TODO maybe also try e.g. temperature=1.5

    out = model.generate(
            tokenized_poet_start, 
            max_length=256,
            do_sample=True,
            top_p=0.9,
            no_repeat_ngram_size=2,
            early_stopping=True,
            pad_token_id= tokenizer.pad_token_id,
            eos_token_id = tokenizer.eos_token_id
            )

    # Decode Poet
    decoded_cont = tokenizer.decode(out[0], skip_special_tokens=True)

    print(decoded_cont)

