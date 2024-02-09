#!/usr/bin/env python3
#coding: utf-8

import common
import os
import cgi

common.header()

form = cgi.FieldStorage()
typ = form.getvalue("typ", "")

if typ == 'admin':
    common.write_out_file(f'gallery_admin_head.html')
common.write_out_file(f'gallery_head.html')

files = os.listdir('genouts')
files.sort(reverse=True)
for filename in files:
    common.write_out_file(f'genouts/{filename}')
    if typ == 'admin':
        key, _ = filename.split('.')
        common.replace_and_write_out_file(
                'gallery_admin_sharebutton.html', {'KEY': key})
    common.write_out_file(f'gallery_sep.html')
    
common.footer()
