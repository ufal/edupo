#!/usr/bin/env python3
#coding: utf-8

import requests

base_url = 'http://quest.ms.mff.cuni.cz/edupo-api/'

poemid = None

def run_request(method, params={}, headers={'accept': 'application/json'}):
    return requests.post(f"{base_url}/{method}", data=params, headers=headers).json()

def test_generate():
    global poemid
    result = run_request('gen')
    assert 'id' in result
    poemid = result['id']

def test_show():
    result = run_request('show', {'poemid': poemid})
    assert 'plaintext' in result

def test_analyze():
    result = run_request('analyze', {'poemid': poemid})
    assert 'body' in result

def test_tts():
    result = run_request('gentts', {'poemid': poemid})
    assert 'url' in result

def test_img():
    result = run_request('genimage', {'poemid': poemid})
    assert 'url' in result

def test_motives():
    result = run_request('genmotives', {'poemid': poemid})
    assert 'motives' in result


