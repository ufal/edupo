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
    data = {'text': text, 'author': 'Rudolf Mayer', 'title': title}
    response = requests.post(f"{base_url}/input", data=data, headers=headers)
    poemid = response.json()['id']

    data = {'poemid': poemid}
    response = requests.post(f"{base_url}/genmotives", data=data, headers=headers)
    motives = response.json()['motives']
    return motives

title=None
text=list()

prevline = ''

for line in sys.stdin:
    line = line.strip()
    if line and (prevline == line):
        if not title is None:
            plaintext = "\n".join(text)
            logging.info(f"GENMOTIVES FOR {title} {repr(plaintext)}")
            motives = analyze(plaintext, title)
            print(f'<h1>{title}</h1>')
            print(*text, sep="<br>")
            print('<h2>MOTIVY:</h2>')
            print(*motives, sep="<br>")

        title = line
        text=list()
    else:
        text.append(prevline)
        prevline = line

