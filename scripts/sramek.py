#!/usr/bin/env python3
#coding: utf-8

import sys

import logging
logging.basicConfig(
    format='%(asctime)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO)

import requests

base_url = 'https://quest.ms.mff.cuni.cz/edupo/'
# base_url = 'http://127.0.0.1:5000/'

headers = {"accept": "application/json"}

def writeout(title, text, motives):
    print(title)
    print(text)
    print('MOTIVY:')
    print(*motives, sep="\n")

def analyze(text, title):
    text = "\n".join(text).strip()
    logging.info(f"GENMOTIVES FOR {title} {repr(text)}")
    
    data = {'text': text, 'author': 'František Ladislav Čelakovský', 'title': title}
    response = requests.post(f"{base_url}/input", data=data, headers=headers)
    poemid = response.json()['id']

    data = {'poemid': poemid}
    response = requests.post(f"{base_url}/genmotives", data=data, headers=headers)
    motives = response.json()['motives']
    
    writeout(title, text, motives)
    return motives


import re

title=None
text=list()

stopwords = {
    'div2>', '<pageNum>', '<subheadPoem>', '<datelinePoem>',
    '<datelinePoemAdd>', '<pageNumAdd>'
        }

for line in sys.stdin:
    line = line.strip()
    if '<list>' in line:
        analyze(text, title)
        break
    if '<headPoem>' in line:
        if not title is None:
            analyze(text, title)


        m = re.search(r'<headPoem>(.*)</headPoem>', line)
        if not m:
            logging.error(f"BAD LINE: {line}")
        title = m.group(1)
        text=list()
    else:
        if not title is None:
            ok = True
            for stop in stopwords:
                if stop in line:
                    ok = False
            if ok:
                line = re.sub(r'(<(corrEd|foreign|abbr|num)>)([^<]*)</\2>', r'\3', line)
                text.append(line)
                if '<' in line:
                    logging.warning(f'!!! {line}')


