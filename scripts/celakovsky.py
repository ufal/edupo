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

def analyze(text, title):
    data = {'text': text, 'author': 'František Ladislav Čelakovský', 'title': title}
    response = requests.post(f"{base_url}/input", data=data, headers=headers)
    poemid = response.json()['id']

    data = {'poemid': poemid}
    response = requests.post(f"{base_url}/genmotives", data=data, headers=headers)
    motives = response.json()['motives']
    return motives

title=None
text=list()

for line in sys.stdin:
    line = line.strip()
    if line.startswith("TITLE"):
        if not title is None:
            text = "\n".join(text)
            logging,info(f"GENMOTIVES FOR {title} {repr(text)}")
            motives = analyze(text, title)
            print(title)
            print(text)
            print('MOTIVY:')
            print(*motives, sep="\n")

        _, title = line.split(' ', 1)
        text=list()
    else:
        text.append(line)


