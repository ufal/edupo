#!/usr/bin/env python3
#coding: utf-8

import requests

base_url = 'http://quest.ms.mff.cuni.cz/edupo-api/'

poemid = None

text = """Sedí hruška v širém poli,
vršek se jí zelená,
pod ní se pase kůň vraný
pase ho má milá."""

def run_request(method, params={}, headers={'accept': 'application/json'}):
    return requests.post(f"{base_url}/{method}", data=params, headers=headers).json()

def test_analyze():
    global poemid
    result = run_request('analyze', {'text': text})
    assert 'id' in result
    poemid = result['id']

def test_show():
    result = run_request('show', {'poemid': poemid})
    assert 'body' in result

def test_tts():
    result = run_request('gentts', {'poemid': poemid})
    assert 'url' in result

"""
def test_img():
    result = run_request('genimage', {'poemid': poemid})
    assert 'url' in result

def test_motives():
    result = run_request('genmotives', {'poemid': poemid})
    assert 'motives' in result
"""

