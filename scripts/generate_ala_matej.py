#!/usr/bin/env python3
#coding: utf-8

import sys

import logging
logging.basicConfig(
    format='%(asctime)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO)

import requests
import json

base_url = 'https://quest.ms.mff.cuni.cz/edupo-api/'
# base_url = 'http://127.0.0.1:5000/'

headers = {"accept": "application/json"}

# base test
# response = requests.get(f"{base_url}/prdel", headers=headers)
# response.encoding='utf8'
# print(response.text)


data = {
        # MODEL
        'modelspec': 'gpt-4o-mini', 
        


        # MATEJOVY PARAMETRE
        
        # old / modern / contemporary / ''
        'old_style': 'old',
        
        # short / long / ''
        'syllables_count': 'short', 
        
        # short / medium / ''
        'poem_length': 'short',
        
        # láska / příroda / město / rodina / čas / []
        'motives': ['láska'],
        
        # veselá / smutná / ''
        'mood': 'veselá',

        # yes / no / ''
        'rhymed': 'yes', 



        # PEVNÉ PARAMETRY, ASI NECHAT TAKTO
        'temperature': 0.7,
        'max_strophes': 2, 
        
        }


logging.info(f"Generate with params: {data}")
response = requests.post(f"{base_url}/gen", data=data, headers=headers)
# response.encoding='utf8'
poemid = response.json()['id']
logging.info(f"Generated poem {poemid}")
# text = response.json()['plaintext']
# print('GENERATED', text, sep="\n")

logging.info(f"Analyzing poem {poemid}")
response = requests.post(f"{base_url}/analyze", data={"poemid": poemid}, headers=headers)
j = response.json()
logging.info(f"Meaning: {j['measures']['chatgpt_meaning']}")
logging.info(f"Unknown words: {j['measures']['unknown_words']}")
logging.info(f"Rhyming: {j['measures']['rhyming']}")
logging.info(f"Rhyming consistency: {j['measures']['rhyming_consistency']}")
# input parameters jsou v j['geninput']


JAKEM = {
    '': 'libovolném',
    'old': 'starém',
    'modern': 'novém',
    'contemporary': 'současném',
}

RYM = {
    'yes': 's rýmem',
    'no': 'bez rýmu',
    '': '(rýmování neurčeno)',
}

with open(poemid + '.json', 'w') as outfile:
    json.dump(j, outfile, indent=4, ensure_ascii=False)
with open(poemid + '.txt', 'w') as outfile:
    jakem = JAKEM[data['old_style']]
    rymovana = RYM[data['rhymed']]
    zadani = f"Zadání: báseň v {jakem} stylu {rymovana}\n\n"
    # ostatní parametry asi nemusíme vypisovat pro hodnocení?
    print(zadani + j['plaintext'], file=outfile)
logging.info(f"Stored poem {poemid}.json and {poemid}.txt")



