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


data = {'rhyme_scheme': 'ABBA', 'metre': 'J'}

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

with open(poemid + '.json', 'w') as outfile:
    json.dump(j, outfile, indent=4, ensure_ascii=False)
logging.info(f"Stored poem {poemid}.json")



