#!/usr/bin/env python3
#coding: utf-8

import common
import os

common.header()

print('<a href="index.py">Zpátky na začátek</a>')
print('<br>')
print('<a href="slideshow.py">Slideshow</a>')
print('<br>')

files = os.listdir('genouts')
files.sort(reverse=True)
for filename in files:
    common.write_out_file(f'genouts/{filename}')
    print('<br><hr><br>')
    
common.footer()
