#!/usr/bin/env python3
#coding: utf-8

import sys
import cgi
from image_generation import get_image_for_line
import random
import common

common.header()

form = cgi.FieldStorage()
typ = form.getvalue("typ", "")
prefix = form.getvalue("prefix", "")
text = form.getvalue("text", "")

# TODO check if data filled in

prompt = prefix + text
image_filename = get_image_for_line(prompt)

# TODO check for errors

with open('result_image.html') as infile:
    html = infile.read()
    html.replace('DEFAULTIMAGE', image_filename)
    print(html)

common.footer()
