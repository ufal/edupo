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
base_url = 'http://127.0.0.1:5000/'

if False:
    print('BASE')
    response = requests.get(f"{base_url}/prdel")
    response.encoding='utf8'
    print(response.text)
    print(response.headers['Content-Type'])
    #print(response.json())

    print('JSON')
    headers = {"accept": "application/json"}
    response = requests.get(f"{base_url}/prdel", headers=headers)
    response.encoding='utf8'
    print(response.text)
    print(response.headers['Content-Type'])

    print('HTML')
    headers = {"accept": "text/html"}
    response = requests.get(f"{base_url}/prdel", headers=headers)
    response.encoding='utf8'
    print(response.text)
    print(response.headers['Content-Type'])


    print('TEXT')
    headers = {"accept": "text/plain"}
    response = requests.get(f"{base_url}/prdel", headers=headers)
    response.encoding='utf8'
    print(response.text)
    print(response.headers['Content-Type'])

if False:
    data = {"poemid": "78467"}
    headers = {"accept": "text/plain"}
    headers = {"accept": "application/json"}
    response = requests.post(f"{base_url}/show", data=data, headers=headers)
    response.encoding='utf8'
    #print(response.text)
    print(response.json())

if True:
    data = {'rhyme_scheme': 'ABBA', 'metre': 'J'}
    headers = {"accept": "text/plain"}
    #headers = {"accept": "application/json"}
    response = requests.post(f"{base_url}/gen", data=data, headers=headers)
    response.encoding='utf8'
    print(response.text)
    #print(response.json())

