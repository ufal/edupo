#!/usr/bin/env python3
#coding: utf-8

import sys
import json
import re

import logging
logging.basicConfig(
    format='%(asctime)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO)

sys.path.append("../backend")
from openai_helper import generate_with_openai_simple

def call_genmotives(filebase, dirname='.'):
    if filebase.endswith('.json'):
        filebase = filebase[:-5]

    filebase = f'{dirname}/{filebase}'

    logging.info(f'Generate motives for {filebase}')

    with open(f'{filebase}.txt') as infile:
        text = infile.read()

    with open(f'{filebase}.json') as infile:
        data = json.load(infile)
        title = data[0]['biblio']['p_title']

    basne = 'básně'
    if title and not 'Bez názvu' in title:
        basne = f"básně {title}"
    
    system = f"Jste literární vědec se zaměřením na poezii. Vaším úkolem je určit až 5 hlavních témat {basne}. Napište pouze tato témata, nic jiného, každé na samostatný řádek. Takto:\n 1. A\n 2. B\n 3. C"
        
    motives = generate_with_openai_simple(text, system)
        
    motives_list = motives.split("\n")
    motives_cleaned = [re.sub(r'^\s*\d+\.\s*', '', item).strip() for item in motives_list]
        
    with open(f'{filebase}.motives', 'w') as outfile:
        json.dump(motives_cleaned, outfile, ensure_ascii=False)

    logging.info(f'Generated motives: {motives_cleaned}')
    
    return motives_cleaned

if __name__=="__main__":
    with open(sys.argv[1]) as inlist:
        for filename in inlist:
            call_genmotives(filename.strip(), dirname=sys.argv[2])
     
