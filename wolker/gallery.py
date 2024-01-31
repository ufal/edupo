#!/usr/bin/env python3
#coding: utf-8

import common
import os
import cgi

common.header()

form = cgi.FieldStorage()
typ = form.getvalue("typ", "")

if typ == 'admin':
    print('''<div id="fb-root"></div>
    <script async defer crossorigin="anonymous"
    src="https://connect.facebook.net/cs_CZ/sdk.js#xfbml=1&version=v19.0&appId=184130128287110"
    nonce="hJb6HzSN"></script>''')

print('<a href="index.py">Zpátky na začátek</a>')
print('<br>')

files = os.listdir('genouts')
files.sort(reverse=True)
for filename in files:
    common.write_out_file(f'genouts/{filename}')
    if typ == 'admin':
        print('<br>')
        print(f'''
<div class="fb-share-button" data-href="https://ufal.mff.cuni.cz/AIvK/edupo/wolker/post.py?key={key}" data-layout="" data-size=""><a target="_blank" href="https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fufal.mff.cuni.cz%2FAIvK%2Fedupo%2Fwolker%2Fpost.py%3Fkey%3D{key}&amp;src=sdkpreparse" class="fb-xfbml-parse-ignore">Sdílet</a></div>
''')
    print('<br><hr><br>')
    
common.footer()
