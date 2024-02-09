#!/usr/bin/env python3
#coding: utf-8

import cgi
import common
import wolker_interactive

common.header()

# get inputs
form = cgi.FieldStorage()
thread_id = form.getvalue("thread_id", "")
if thread_id:
    messages, roles = wolker_interactive.get_thread_messages(thread_id)
else:
    messages, roles = [], []

def append(result, field, value):
    html = common.replace_and_return_file(f'share_{field}.html', {'CONTENT': value})
    result.append(html)

def get_append(result, field, form):
    value = form.getvalue(field, None)
    if value:
        append(result, field, value)

# construct result
result = []
get_append(result, 'title', form)
get_append(result, 'text', form)
for message, role in zip(messages, roles):
    append(result, f'message_{role}', common.nl2br(message))
get_append(result, 'image', form)
get_append(result, 'author', form)

# write out into file
filename_out = common.get_filename()
with open(f'genouts/{filename_out}.html', 'w') as outfile:
    print(*result, sep='\n', file=outfile)

# get and show sharing QR code
import qrcode
url = f'https://ufal.mff.cuni.cz/AIvK/edupo/wolker/post.py?key={filename_out}'
img = qrcode.make(url)
img.save(f'qrcodes/{filename_out}.png')
common.replace_and_write_out_file('share.html', {'KEY': filename_out})

common.footer()
