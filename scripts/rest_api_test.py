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

if False:
    data = {'rhyme_scheme': 'ABBA', 'metre': 'J'}
    headers = {"accept": "text/plain"}
    #headers = {"accept": "application/json"}
    response = requests.post(f"{base_url}/gen", data=data, headers=headers)
    response.encoding='utf8'
    print(response.text)
    #print(response.json())

if True:
    headers = {"accept": "application/json"}

    data = {}
    response = requests.post(f"{base_url}/gen", data=data, headers=headers)
    poemid = response.json()['id']
    text = response.json()['plaintext']
    print('GENERATED', text, sep="\n")

    data = {"poemid": poemid}
    response = requests.post(f"{base_url}/analyze", data=data, headers=headers)
    # TODO show some output
    print('ANALYZED', poemid)
    
    response = requests.post(f"{base_url}/genmotives", data=data, headers=headers)
    motives = response.json()['motives']
    print('MOTIVES', *motives, sep="\n")

    response = requests.post(f"{base_url}/genimage", data=data, headers=headers)
    url = response.json()['url']
    print('IMAGE', base_url+url)

    response = requests.post(f"{base_url}/gentts", data=data, headers=headers)
    url = response.json()['url']
    print('TTS', base_url+url)

if False:
    headers = {"accept": "application/json"}

    data = {'text': 'Matce pro kacířství syna vzali,\nna jesuitu jej vychovali;', 'author': 'Rokyta', 'title': 'Buben'}
    response = requests.post(f"{base_url}/input", data=data, headers=headers)
    poemid = response.json()['id']
    print('ID', poemid, sep="\n")

    data = {"poemid": poemid}
    response = requests.post(f"{base_url}/analyze", data=data, headers=headers)
    # TODO show some output
    print('ANALYZED') 
    
    response = requests.post(f"{base_url}/genmotives", data=data, headers=headers)
    motives = response.json()['motives']
    print('MOTIVES', *motives, sep="\n")

    response = requests.post(f"{base_url}/genimage", data=data, headers=headers)
    url = response.json()['url']
    print('IMAGE', base_url+url)

    response = requests.post(f"{base_url}/gentts", data=data, headers=headers)
    url = response.json()['url']
    print('TTS', base_url+url)


