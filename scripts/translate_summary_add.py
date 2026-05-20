#!/usr/bin/env python3
#coding: utf-8

import sys

import logging
logging.basicConfig(
    format='%(asctime)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO)

import json

# Reads in file
# Translates summary from en to cs
# Stores result in the file as cs_sumarization

filename = sys.argv[1]

logging.info(f"Filename: {filename}")

with open(filename) as infile:
    j = json.load(infile)

s = j[0]["sumarization"]

logging.info(f"Original summary: {s}")

import requests
url = 'http://lindat.mff.cuni.cz/services/translation/api/v2/models/en-cs'
data = {"input_text": s}
headers = {"accept": "text/plain"}
response = requests.post(url, data = data, headers = headers)
response.encoding='utf8'

s_cs = response.text

logging.info(f"Translated summary: {s_cs}")

j[0]["cs_sumarization_trans"] = s_cs

with open(filename, 'w') as outfile:
    json.dump(j, outfile)

