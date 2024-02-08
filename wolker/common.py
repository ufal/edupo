#!/usr/bin/env python3
#coding: utf-8

import sys
import random
import cgi
from datetime import datetime

def get_filename():
    return datetime.now().strftime("%Y%m%d%H%M%S")
    # + random.randrange(10000000, 100000000) ... randseed je time takže bych potřeboval seed

def write_out_file(filename):
    with open(filename) as infile:
        print(infile.read())

def replace_and_write_out_file(filename=None, replacements={}):
    if not replacements:
        replacements = get_replacements()
    if not filename:
        filename = replacements.get('PAGE', 'welcome')
        filename += '.html'
        # TODO CHECK!!!!
    with open(filename) as infile:
        text = infile.read()
        for key in replacements:
            text = text.replace(key, replacements[key])
        print(text)

def header(subtype=''):
    print("Content-type: text/html")
    print()
    write_out_file(f'header{subtype}.html')

def footer():
    write_out_file('footer.html')

def nl2br(text):
    return text.replace('\n', '<br>')

def get_replacements(names=[]):
    replacements = {}
    form = cgi.FieldStorage()
    if not names:
        names = form.getvalue('replacements', [])
    for name in names:
        value = form.getvalue(name, "")
        replacements[name.upper()] = value
    return replacements


