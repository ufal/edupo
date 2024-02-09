#!/usr/bin/env python3
#coding: utf-8

import cgi
from image_generation import get_image_for_line
import common

common.header()

form = cgi.FieldStorage()
title = form.getvalue("title", "")
prefix = form.getvalue("prefix", "")
text = form.getvalue("text", "")

prompt = f"{title} {prefix} {text}"
print(f'<!-- {prompt} -->')

# generate the image
# TODO check for errors
image = get_image_for_line(prompt)

replacements = common.get_replacements(
        form, ['image', 'thread_id', 'text', 'title', 'back'])
replacements['IMAGE'] = image

common.replace_and_write_out_file('result_image.html', replacements)

if replacements['BACK']:
    common.replace_and_write_out_file('result_image_backlink.html', replacements)

common.footer()
