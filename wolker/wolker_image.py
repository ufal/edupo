#!/usr/bin/env python3
#coding: utf-8

import sys
import cgi
from image_generation import get_image_for_line
import common

common.header()

form = cgi.FieldStorage()
prefix = form.getvalue("prefix", "")
title = form.getvalue("title", "")
text = form.getvalue("text", "")
thread_id = form.getvalue("thread_id", "")
back = form.getvalue("back", "")

# TODO check if data filled in

prompt = prefix + text
if title:
    prompt += f' The image accompanies the text called: {title}'
print(f'<!-- {prompt} -->')

image = get_image_for_line(prompt)

# TODO check for errors

replacements = {
        'DEFAULTIMAGE': image,
        'THREAD_ID': thread_id,
        'TEXT': text,
        'TITLE': title,
        'BACK': back,
        }

common.replace_and_write_out_file('result_image.html', replacements)

if back:
    common.replace_and_write_out_file('result_image_backlink.html', replacements)

common.footer()
