#!/usr/bin/env python3
#coding: utf-8

import requests

base_url = 'http://quest.ms.mff.cuni.cz/edupo-api/'
text = 'Hello, Kyselá Prdel!'

def run_request_post(params={}, headers={}):
    return requests.post(f"{base_url}/prdel", data=params, headers=headers)

def run_request_get(params={}, headers={}):
    return requests.get(f"{base_url}/prdel", params=params, headers=headers)

def test_prdel_basic():
    response = run_request_get()
    assert response.ok

def test_prdel_basic_post():
    response = run_request_post()
    assert response.ok

def test_prdel_html():
    response = run_request_post()
    assert response.text == f'<p>{text}</p>'

def test_prdel_json_param():
    response = run_request_post({'accept': 'json'})
    assert response.json() == {'text': text}

def test_prdel_json_headers():
    headers = {"accept": "application/json"}
    response = run_request_post({}, headers)
    assert response.json() == {'text': text}

def test_prdel_text_params():
    response = run_request_post({'accept': 'txt'})
    assert response.text == text + '\n'

def test_prdel_text_headers():
    headers = {"accept": "text/plain"}
    response = run_request_post({}, headers)
    assert response.text == text + '\n'



