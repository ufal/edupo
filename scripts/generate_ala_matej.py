#!/usr/bin/env python3
#coding: utf-8

import sys
import time
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

def generate_poem(data, filename):
    
    start_time = time.perf_counter()
    logging.info(f"Generate with params: {data}")
    response = requests.post(f"{base_url}/gen", data=data, headers=headers)
    # response.encoding='utf8'
    poemid = response.json()['id']
    logging.info(f"Generated poem {poemid}")
    # text = response.json()['plaintext']
    # print('GENERATED', text, sep="\n")
    end_time = time.perf_counter()

    logging.info(f"Analyzing poem {poemid}")
    response = requests.post(f"{base_url}/analyze", data={"poemid": poemid}, headers=headers)
    j = response.json()

    # add time to measures
    j['measures']['time'] = end_time - start_time

    #logging.info(f"Meaning: {j['measures']['chatgpt_meaning']}")
    #logging.info(f"Unknown words: {j['measures']['unknown_words']}")
    #logging.info(f"Rhyming: {j['measures']['rhyming']}")
    #logging.info(f"Rhyming consistency: {j['measures']['rhyming_consistency']}")
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
   
    with open(filename + '.json', 'w') as outfile:
        json.dump(j, outfile, indent=4, ensure_ascii=False)
    with open(filename + '.txt', 'w') as outfile:
        jakem = JAKEM[data['old_style']]
        rymovana = RYM[data['rhymed']]
        zadani = f"Zadání: báseň v {jakem} stylu {rymovana}\n\n"
        # ostatní parametry asi nemusíme vypisovat pro hodnocení?
        print(zadani + j['plaintext'], file=outfile)
        logging.info(f"Stored poem {poemid}.json and {poemid}.txt")
   
    return j['measures']




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

model = 'gpt-4o-mini'
directory = '/net/projects/EduPo/data/DM_generovane'


poem_counter = 0
avg_measures = {'chatgpt_meaning': 0, 'rhyming': 0, 'unknown_words': 0, 'time': 0}

for old_style in [ "old", "modern", "contemporary", "" ]:
    for syllables_count in [ "short", "long", "" ]:
        for poem_length in [ "short", "medium", "" ]:
            for motives in [ ["láska"] , ["příroda"], ["město"], ["rodina"], ["čas"], [] ]:
                for mood in [ "veselá", "smutná", "" ]:
                    for rhymed in [ "yes", "no", "" ]:
                        data = {
                            'modelspec': model,
                            'old_style': old_style,
                            'syllables_count': syllables_count, 
                            'poem_length': poem_length,
                            'motives': motives,
                            'mood': mood,
                            'rhymed': rhymed, 
                            'temperature': 0.7,
                            'max_strophes': 2, 
                            }
                        poem_counter += 1
                        filename = directory + '/' + model + '-' + str(poem_counter)
                        measures = generate_poem(data, filename)
                        for m in avg_measures.keys():
                            avg_measures[m] += measures[m]

for m in avg_measures.keys():
    print(m, str(avg_measures[m] / poem_counter))
                        


