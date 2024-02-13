#!/usr/bin/env python3
#coding: utf-8

import random
import cgi
import os
import os.path
import random
from datetime import datetime
from image_generation import get_image_for_line
import wolker_interactive
import html

OUTPUTDIR = 'genouts'
OUTPUTDIRP = 'genoutsp'
DEFAULTPAGE = 'intro'

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
            value = BR2br(html.escape(replacements[key], quote=True))
            text = text.replace(key, value)
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

def footer(subtype=''):
    write_out_file(f'footer{subtype}.html')

def nl2BR(text):
    return text.replace('\n', '[BR]')

def BR2br(text):
    return text.replace('[BR]', '<br>')

import re
def remove_refs(text):
    # 【11†zdroj】
    return re.sub(r'【[^】]*】', '', text)

# for handling bottle
def page(page=None, replacements={}):
    header = return_file('header.html')
    body = _replace_and_return_file(page, replacements)
    footer = return_file('footer.html')
    return header, body, footer

def indexpage():
    header = return_file('header_static.html')
    body = return_file('intro.html')
    footer = return_file('footer_with_links.html')
    return header, body, footer

def creditspublic():
    header = return_file('header_static.html')
    body = return_file('credits.html')
    footer = return_file('footer_public.html')
    return header, body, footer

# show public post
def post(key):
    header = return_file('header_static.html')
    
    filename = f'{OUTPUTDIRP}/{key}.html'
    if key and key.isnumeric() and os.path.isfile(filename):
        body = return_file(filename)
    else:
        body = f"Nelze zobrazit soubor se zadaným klíčem '{key}'"

    footer = return_file('footer_public.html')

    return header, body, footer

# slideshow
def getctime(item):
    item_path = os.path.join(OUTPUTDIR, item)
    return os.path.getctime(item_path)

def slideshow_choose_candidate():
    candidates = os.listdir(OUTPUTDIR)
    if not candidates:
        return 'empty_gallery.html'

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
    files.append(return_file('header_static.html'))
    
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

def prompt_in_comment(prompt):
    escaped_prompt = prompt.replace('>', ' >')
    return f'<!-- {escaped_prompt} -->'

import poems
def get_poem_htmls_KARUSEL_UNUSED():
    poem_tuples = poems.poems()
    poem_htmls = []
    poemid = 0
    for title, text in poem_tuples:
        replacements = {
                'POEMID': str(poemid),
                'TITLE': title,
                'TEXT': text}
        poem_htmls.append(_replace_and_return_file('poem.html', replacements))
        poemid += 1
    return poem_htmls

def get_poem_htmls():
    poem_titles = poems.titles()
    poem_htmls = []
    for title in poem_titles:
        replacements = {'TITLE': title}
        poem_htmls.append(_replace_and_return_file('poemoption.html', replacements))
    return poem_htmls

def wolker_feel(title='', text=''):
    poem_htmls = get_poem_htmls()
    replacements = {
            'TITLE': title,
            'TEXT': text,
            'COUNT': str(len(poem_htmls))}
    header = return_file('header.html')
    body = _replace_and_return_file(
            'welcome_wolker_feel.html', replacements
            ).replace('POEMS', '\n'.join(poem_htmls))
    footer = return_file('footer.html')
    return header, body, footer

def error(message=''):
    files = []
    files.append(return_file('header.html'))
    files.append(replace_and_return_file('error.html', {'ERROR': message}))
    files.append(return_file('footer.html'))
    return files

def wolker_image(title, prefix, text, replacements):
    files = []
    files.append(return_file('header.html'))

    if title:
        title = f"{title}: "
    prompt = f"{title}{prefix}{text}"

    files.append(prompt_in_comment(prompt))
    try:
        image, prompt = get_image_for_line(prompt)
    except Exception as e:
        return error(str(e))
    files.append(prompt_in_comment(prompt))
    replacements['IMAGE'] = image
    
    conversation = []
    if replacements['THREAD_ID']:
        messages, roles = wolker_interactive.get_thread_messages(replacements['THREAD_ID'])
        for message, role in zip(messages, roles):
            conversation.append(replace_and_return_file(
                f'wolker_chat_message_{role}.html',
                {'CONTENT': remove_refs(nl2BR(message))}))

    files.append(replace_and_return_file(
        'result_image.html', replacements).replace(
            'CONVERSATION', '\n'.join(conversation)))
    if replacements['PREVFULL']:
        files.append(replace_and_return_file(
            'result_image_backfulllink.html', replacements))
    elif replacements['BACK']:
        files.append(replace_and_return_file(
            'result_image_backlink.html', replacements))
    files.append(return_file('footer.html'))
    
    return files

typ2text = {
        'chat': 'Konverzace na téma',
        'cowrite': 'Báseň na téma',
        'essay': 'Úvaha na téma',
        'poem': 'Báseň na téma',
        }

typ2command = {
        'chat': 'Odpovědět',
        'cowrite': 'Dokonči verš',
        }


def wolker_chat(text='', typ='poem', title='', assistant_id='asst_oEwl7wnhGDi5JDvAdE92GgWk', thread_id=None):
    """Chat with Wolker persona.

    text = user input
    typ = chat/cowrite/essay/poem
    title = 'Báseň na téma ...'
    """
    files = []

    if not title:
        title = f'{typ2text[typ]} {text}'

    # invoke the chatbot
    try:
        messages, roles, thread_id = wolker_interactive.talk_threaded(
            text, assistant_id, thread_id)
    except Exception as e:
        return error(str(e))

    # compose the page
    files.append(return_file('header.html'))
    files.append(replace_and_return_file(
        'wolker_chat_head.html', {}))
    for message, role in zip(messages, roles):
        # role is user or assistant
        files.append(replace_and_return_file(
            f'wolker_chat_message_{role}.html',
            {'CONTENT': remove_refs(nl2BR(message))}))
    files.append(replace_and_return_file(
        'wolker_chat_footer.html', {}))
    if typ in ('chat', 'cowrite'):
        files.append(replace_and_return_file(
            'wolker_chat_controls.html', {
                'COMMAND': typ2command[typ],
                'THREAD_ID': thread_id,
                'ASSISTANT_ID': assistant_id,
                'TITLE': title,
                'TYP': typ,
                }))
    files.append(replace_and_return_file(
        'wolker_chat_share.html', {
            'THREAD_ID': thread_id,
            'TITLE': title,
            }))
    files.append(return_file('footer.html'))
    
    return files

# form is something which can get the following keys:
# thread_id, title, text, image, author
# either directly cgi form, or a dict gotten throgh getunicode from bottle
def share_page(form):
    result = []

    def append(field, value):
        text = replace_and_return_file(
                f'share_{field}.html',
                {'CONTENT': remove_refs(nl2BR(value))})
        result.append(text)

    def get_append(field):
        value = form.get(field, None)
        if value:
            append(field, value)

    if form['thread_id']:
        messages, roles = wolker_interactive.get_thread_messages(form['thread_id'])
    else:
        messages, roles = [], []
    
    # if there is text but not title, use text as title
    if form['text'] and not form['title']:
        form['title'] = form['text']
        form['text'] = ''

    # construct result
    get_append('title')
    get_append('text')
    for message, role in zip(messages, roles):
        append(f'message_{role}', message)
    get_append('image')
    get_append('author')

    # write out into file
    filename_out = get_filename()
    with open(f'{OUTPUTDIR}/{filename_out}.html', 'w') as outfile:
        print(*result, sep='\n', file=outfile)
    with open(f'{OUTPUTDIRP}/{filename_out}.html', 'w') as outfile:
        print(*result, sep='\n', file=outfile)

    # get and show sharing QR code
    import qrcode
    base_url = return_file('share_baseurl.txt').strip()
    url = f'{base_url}{filename_out}'
    img = qrcode.make(url)
    img.save(f'qrcodes/{filename_out}.png')

    files=[]
    files.append(return_file('header.html'))
    files.append(replace_and_return_file('share.html', {'KEY': filename_out}))
    files.append(return_file('footer.html'))

    return files

