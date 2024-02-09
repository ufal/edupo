#!/usr/bin/env python3
#coding: utf-8

import random
import cgi
import os
import os.path
import random
from datetime import datetime
from image_generation import get_image_for_line

OUTPUTDIR = 'genouts'
DEFAULTPAGE = 'welcome'

def get_filename():
    return datetime.now().strftime("%Y%m%d%H%M%S")
    # + random.randrange(10000000, 100000000) ... randseed je time takže bych potřeboval seed

def return_file(filename):
    with open(filename) as infile:
        return infile.read()

def write_out_file(filename):
    with open(filename) as infile:
        print(infile.read())

def get_replacements(form, names=None):
    replacements = {}
    if not names:
        names = form.getvalue('replacements', '').split(',')
    for name in names:
        replacements[name.upper()] = form.getvalue(name, "")
    return replacements

def _replace_and_return_file(filename, replacements):
    with open(filename) as infile:
        text = infile.read()
        for key in replacements:
            text = text.replace(key, replacements[key])
        return text

def replace_and_write_out_file(filename=None, replacements={}):
    print(replace_and_return_file(filename, replacements))

def replace_and_return_file(filename=None, replacements={}):
    if not filename:
        # get from parameters
        # WARNING: this eats up the parameters for everyone!
        assert not replacements
        
        form = cgi.FieldStorage()
        
        # filename: get from page
        filename = form.getvalue('page', DEFAULTPAGE)
        if not filename.isidentifier():
            filename = DEFAULTPAGE
        filename += '.html'
    
        # replacements: get from replacements
        replacements = get_replacements(form)

    return _replace_and_return_file(filename, replacements)
   
def httpheader():
    print("Content-type: text/html")
    print()

def header(subtype=''):
    print("Content-type: text/html")
    print()
    write_out_file(f'header{subtype}.html')

def footer():
    write_out_file('footer.html')

def nl2br(text):
    return text.replace('\n', '<br>')

# for handling bottle
def page(page=None, replacements={}):
    header = return_file('header.html')
    body = _replace_and_return_file(page, replacements)
    footer = return_file('footer.html')
    return header, body, footer

# show public post
def post(key):
    header = return_file('header_static.html')
    
    filename = f'{OUTPUTDIR}/{key}.html'
    if key and key.isnumeric() and os.path.isfile(filename):
        body = return_file(filename)
    else:
        body = f"Nelze zobrazit soubor se zadaným klíčem '{key}'"

    footer = return_file('footer.html')

    return header, body, footer

# slideshow
def getctime(item):
    item_path = os.path.join(OUTPUTDIR, item)
    return os.path.getctime(item_path)

def slideshow_choose_candidate():
    candidates = os.listdir(OUTPUTDIR)

    # randomly choose whether to use weights or not
    if random.randint(0, 1) == 0:
        candidate = random.choice(candidates)
    else:
        # assert == 1
        candidates.sort(key=getctime, reverse=True)
        weights = []
        weight = 1
        decay = 0.7
        for candidate in candidates:
            weights.append(weight)
            weight *= decay
        candidate = random.choices(candidates, weights=weights)[0]
    
    return f'{OUTPUTDIR}/{candidate}'

def slideshow():
    candidate = slideshow_choose_candidate()
    files = [
        'header_refresh.html',
        candidate,
        'footer.html',
    ]
    return [return_file(f) for f in files]

def gallery(typ=''):
    files = []
    files.append(return_file('header.html'))
    
    if typ == 'admin':
        files.append(return_file('gallery_admin_head.html'))
    files.append(return_file('gallery_head.html'))

    postfiles = os.listdir(OUTPUTDIR)
    postfiles.sort(reverse=True)
    for filename in postfiles:
        files.append(return_file(f'{OUTPUTDIR}/{filename}'))
        if typ == 'admin':
            key, _ = filename.split('.')
            files.append(replace_and_return_file(
                    'gallery_admin_sharebutton.html', {'KEY': key}))
        
            files.append(return_file('gallery_sep.html'))
    files.append(return_file('footer.html'))
    
    return files

def wolker_image(prompt, replacements):
    files = []
    files.append(return_file('header.html'))

    # TODO check for errors
    files.append(f'<!-- {prompt} -->')
    image = get_image_for_line(prompt)
    replacements['IMAGE'] = image
    
    files.append(replace_and_return_file(
        'result_image.html', replacements))
    if replacements['BACK']:
        files.append(replace_and_return_file(
            'result_image_backlink.html', replacements))
    files.append(return_file('footer.html'))
    
    return files

