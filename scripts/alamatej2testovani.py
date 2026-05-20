#!/usr/bin/env python3
#coding: utf-8

import sys
import time
import logging

logging.basicConfig(
    format='%(asctime)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO)

import json

def json2line(filename):
    JAKEM = {
        '': 'libovolném',
        'old': 'starém',
        'modern': 'novém',
        'contemporary': 'současném',
    }

    RYM = {
        'yes': 's rýmem',
        'no': 'bez rýmu',
        '': '(rýmování neurčeno)',
    }
   
    with open(filename, 'r') as infile:
        data = json.load(infile)

        jakem = JAKEM[data['geninput']['old_style']]
        rymovana = RYM[data['geninput']['rhymed']]
        vystup = f"""Zadání: báseň v {jakem} stylu {rymovana}

{data['author_name']}:
{data['title']}


{data['plaintext']}:"""

    return vystup
   

if __name__=="__main__":
    filename = sys.argv[1]
    vystup = json2line(filename)
    print(repr(vystup))

