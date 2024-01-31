#!/usr/bin/env python3
#coding: utf-8

import sys
import random
from datetime import datetime

def get_filename():
    return datetime.now().strftime("%Y%m%d%H%M%S")
    # + random.randrange(10000000, 100000000) ... randseed je time takže bych potřeboval seed

def write_out_file(filename):
    with open(filename) as infile:
        print(infile.read())

def header():
    print("Content-type: text/html")
    print()
    write_out_file('header.html')

def header_refresh():
    print("Content-type: text/html")
    print()
    write_out_file('header_refresh.html')

def footer():
    write_out_file('footer.html')

def nl2br(text):
    return text.replace('\n', '<br>')


