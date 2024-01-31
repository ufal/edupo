#!/usr/bin/env python3
#coding: utf-8

import sys
import cgi
import common
import wolker_interactive

common.header()

form = cgi.FieldStorage()
typ = form.getvalue("typ", "")
image_filename = form.getvalue("image_filename", "")
poemname = form.getvalue("poemname", "")
thread_id = form.getvalue("thread_id", "")

# TODO check if data filled in

result = []
if poemname:
    result.append(f'<h2>{poemname}</h2>')
if thread_id:
    messages, roles = wolker_interactive.get_thread_messages(thread_id)
    for message, role in zip(messages, roles):
        result.append(f'<p class="{role}">{common.nl2br(message)}</p>')
if image_filename:
    result.append(f'<img src="genimgs/{image_filename}.png">')

html = '\n'.join(result)

filename_out = common.get_filename()

with open(f'genouts/{filename_out}.html', 'w') as outfile:
    print(html, file=outfile)

import qrcode
url = f'https://ufal.mff.cuni.cz/AIvK/edupo/wolker/post.py?key={filename_out}'
img = qrcode.make(url)
img.save(f'qrcodes/{filename_out}.png')

common.replace_and_write_out_file('share.html', {'KEY': filename_out})

common.footer()
