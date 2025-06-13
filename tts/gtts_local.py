#!/usr/bin/env python3
#coding: utf-8

import sys

import logging
logging.basicConfig(
    format='%(asctime)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO)


from gtts import gTTS
with open('text.txt') as intext:
    text = intext.read()
    filename = f'gtts.mp3'
    tts = gTTS(text, lang='cs', tld='cz', slow=True)
    # tts = gTTS(text, lang='cs', tld='cz', slow=False)
    tts.save(filename)

