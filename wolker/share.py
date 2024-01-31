#!/usr/bin/env python3
#coding: utf-8

import sys
import cgi
import common

common.header()

form = cgi.FieldStorage()
typ = form.getvalue("typ", "")
image_filename = form.getvalue("image_filename", "")
text = form.getvalue("text", "")

# TODO check if data filled in

if typ == 'image':
    html = f'<img src="genimgs/{image_filename}.png">'
elif typ == 'text':
    html = f'<pre>{text}</pre>'
else:
    assert False

filename_out = common.get_filename()

with open('genouts/{filename_out}.html', 'w') as outfile:
    print(html, file=outfile)

print('<p>Výsledek je nyní veřejně sdílen v <a href="gallery.py">Galerii</a> a je zařazen do projekce v muzeu.</p>')
    
common.footer()
