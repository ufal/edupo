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

with open(filename) as infile:
    j = json.load(infile)

print("SOUBOR:", filename)
print("AUTOR:", j[0]["p_author"]["name"])
print("BÁSEŇ:", j[0]["biblio"]["p_title"])
print("SLOKY:", len(j[0]["body"]))
print()

for stanza in j[0]["body"]:
    for verse in stanza:
        print(verse["text"])
    print()

if 'sumarization' in j[0]:
    print("SHRNUTÍ EN:", j[0]['sumarization'])
    print()

if 'cs_sumarization_trans' in j[0]:
    print("SHRNUTÍ EN -> MT -> CS:", j[0]['cs_sumarization_trans'])
    print()

if 'cs_sumarization' in j[0]:
    print("SHRNUTÍ CS:", j[0]['cs_sumarization'])
    print()

if 'categories' in j[0]:
    c = j[0]['categories']
    if type(c) == str:
        print("KATEGORIE:", c)
    else:
        print("KATEGORIE:", *c)
    print()



