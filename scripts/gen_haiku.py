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


for i in range(1, 16):
    print(f'<h1>Haiku č. {i}</h1>')
    data = {'form': 'haiku', 'modelspec': 'tm'}
    headers = {"accept": "text/plain"}
    #headers = {"accept": "application/json"}
    response = requests.post(f"{base_url}/gen", data=data, headers=headers)
    response.encoding='utf8'
    print(response.text)
    #print(response.json())


