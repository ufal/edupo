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
back = form.getvalue("back", "")
prefix = form.getvalue("prefix", "")
poemname = form.getvalue("poemname", "")
text = form.getvalue("text", "")
thread_id = form.getvalue("thread_id", "")

# TODO check if data filled in

prompt = prefix + text
if poemname:
    prompt += ' The image accompanies the poem called: '
print(f'<!-- {prompt} -->')
image_filename = get_image_for_line(prompt)

# TODO check for errors

replacements = {
        'DEFAULTIMAGE': image_filename,
        'THREAD_ID': thread_id,
        'TEXT': text,
        'POEMNAME': poemname,
        'BACK': back,
        }

common.replace_and_write_out_file('result_image.html', replacements)
common.footer()
