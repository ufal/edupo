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

DEFAULTPAGE = 'welcome'

def replace_and_write_out_file(filename=None, replacements={}):
    print(replace_and_return_file(filename, replacements))

def replace_and_return_file(filename=None, replacements={}):
    if not filename:
        # get from parameters
        # WARNING: this eats up the parameters for everyone!
        assert not replacements
        
        form = cgi.FieldStorage()
        
        # filename: get from page
        filename = form.getvalue('page', DEFAULTPAGE)
        if not filename.isidentifier():
            filename = DEFAULTPAGE
        filename += '.html'
    
        # replacements: get from replacements
        names = form.getvalue('replacements', '').split(',')
        for name in names:
            value = form.getvalue(name, "")
            replacements[name.upper()] = value
    
    with open(filename) as infile:
        text = infile.read()
        for key in replacements:
            text = text.replace(key, replacements[key])
        return text

def header(subtype=''):
    print("Content-type: text/html")
    print()
    write_out_file(f'header{subtype}.html')

def footer():
    write_out_file('footer.html')

def nl2br(text):
    return text.replace('\n', '<br>')


