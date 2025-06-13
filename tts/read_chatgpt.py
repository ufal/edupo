#!/usr/bin/env python3
#coding: utf-8

import sys

import logging
logging.basicConfig(
    format='%(asctime)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO)


with open('text.txt') as intext:
    text = intext.read()

with open('apikey.txt') as intext:
    apikey = intext.read()

filename = f'openai.mp3'


from pathlib import Path
from openai import OpenAI

client = OpenAI(api_key=apikey,)

with client.audio.speech.with_streaming_response.create(
    model="gpt-4o-mini-tts",
    voice="coral",
    input=text,
    #instructions="Speak in a cheerful and positive tone.",
) as response:
    response.stream_to_file(filename)

