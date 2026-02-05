#!/usr/bin/env python3
#coding: utf-8

import sys

import logging
logging.basicConfig(
    format='%(asctime)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO)

import requests

base_url = 'https://quest.ms.mff.cuni.cz/edupo-api/'
# base_url = 'http://127.0.0.1:5000/'

headers = {"accept": "text/plain"}

ids = range(10)


for poemid in ids:
    print(poemid, flush=True)
    data = {"poemid": poemid, "regenerate": "true"}
    response = requests.post(f"{base_url}/guessmood", data=data, headers=headers)
    mood = response.text
    print(mood)

