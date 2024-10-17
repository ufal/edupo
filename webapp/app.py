#!/usr/bin/env python3
#coding: utf-8

from flask import Flask, request, render_template, g, redirect, url_for, jsonify, Response
from itertools import groupby
import os
from gen import generuj
import show_poem_html
import sqlite3
import json
from collections import defaultdict
import re
import random
from openai_helper import *

import sys
sys.path.append("../kveta")
from kveta import okvetuj

app = Flask(__name__)
print(__name__)

DBFILE='/net/projects/EduPo/data/new.db'

# I have not been able to persuade Flask that it is under / locally but under
# /edupo/ externally so this is a work-around
EDUPO_SERVER_PATH = os.getenv('EDUPO_SERVER_PATH', '')

sqlite3.register_converter("json", json.loads)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DBFILE,
                detect_types=sqlite3.PARSE_DECLTYPES)
        db.row_factory = sqlite3.Row
        db.enable_load_extension(True)
        db.load_extension("./regex0")
    return db

# close db connection at end of handling request
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.commit()  # in case commit forgotten
        db.close()

# TODO tohle se asi nemá dělat
# NOTE takhle pokud POSTuju tak se nedostanu k parametrum zadanym v URL; tj.
# nechceme dělat POST z formuláře kde by cílová URL obsahovala i GET parametry
# (to asi stejně nechceme)
def get_post_arg(key, default=None, nonempty=False, isarray=False):
    result = default
    if request.method == 'POST':
        if isarray:
            result = request.form.getlist(key)
        else:
            result = request.form.get(key, default)
    elif request.method == 'GET':
        if isarray:
            result = request.args.getlist(key)
        else:
            result = request.args.get(key, default)
    else:
        # TODO probably should not happen
        assert False, "Unexpected method " + str(request.method)
    if nonempty and not result:
        result = default
    return result

def add_metadata_to_dict(poem, fields=[
    'id', 'author', 'author_name', 'title', 'schools', 'b_title',
    'born', 'died', 'subtitle', 'publisher', 'place', 'year',
    ]):
    for field in fields:
        value = get_post_arg(field, '')
        if value == 'None':
            value = ''
        poem[field] = value
    return poem

# our defined order of priorities:
# 1. HTML (because of web browsers)
# 2. JSON (for APIs)
# 3. TEXT (fallback)
def return_accepted_type(text='', json=None, html=None):
    if html is not None and request.accept_mimetypes.accept_html:
        return html
    elif json is not None and request.accept_mimetypes.accept_json:
        if type(json) == str:
            # already JSON
            return Response(json, mimetype='application/json')
        else:
            return jsonify(json)
    else:
        return Response(text, mimetype='text/plain')

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/prdel")
def prdel_world():
    text = "Hello, Prdel myš!"
    return return_accepted_type(text, {'text': text}, f"<p>{text}</p>")
    # also can use a JSON string as json:
    # return return_accepted_type(text, "{'text': "+text+"}", f"<p>{text}</p>")

@app.route("/gen", methods=['GET', 'POST'])
def call_generuj():
    # empty or 'náhodně' means random
    rhyme_scheme = get_post_arg('rhyme_scheme', '')
    verses_count = int(get_post_arg('verses_count', 0, True))
    syllables_count = int(get_post_arg('syllables_count', 0, True))
    metre = get_post_arg('metre')
    first_words = get_post_arg('first_words', isarray=True, default=[])
    app.logger.warn(first_words)
    first_words = [word.strip() for word in first_words if word.strip() != '']
    app.logger.info(f"Generate poem with '{rhyme_scheme}' scheme, '{metre}' metre, {verses_count} verses, {syllables_count} syllables, starting '{first_words}'")
    poet_start = rhyme_scheme
    raw_output, clean_verses = generuj(
            poet_start, metre, verses_count, syllables_count,
            first_words)
    app.logger.info(f"Generated poem {clean_verses}")
   
    text = "\n".join(clean_verses)
    hash64 = text2id(text)
    poemid = f'{hash64}.txt'
    with open(f'static/poemfiles/{poemid}', 'w') as outfile:
        print(text, file=outfile)

    data = {'clean_verses': clean_verses, 'raw_output': raw_output}

    html = render_template('show_poem_gen.html',
            clean_verses=clean_verses,
            raw='\n'.join(raw_output)
            )
    
    return return_accepted_type(text, data, html)

@app.route("/show", methods=['GET', 'POST'])
def call_show():
    poemid = get_post_arg('poemid', str(random.randint(0,80229)), True)
    if poemid.endswith('.json'):
        data = show_poem_html.show_file(poemid)
    else:
        with get_db() as db:
            sql = 'SELECT *, books.title as b_title FROM poems, books, authors WHERE poems.id=? AND books.id=poems.book_id AND authors.identity=poems.author'
            result = db.execute(sql, (poemid,)).fetchone()
        assert result != None 
        data = show_poem_html.show(result)
    
    # TODO the rendering should be lazy!!!
    # TODO turn this around... maybe each method returns a JSON, and some handling
    # converts it to the right format...?
    html = render_template('show_poem_html.html', **data)
    text = poemdata2text(data)
    
    return return_accepted_type(text, data, html)

@app.route("/showlist", methods=['GET', 'POST'])
def call_showlist():
    with get_db() as db:
        sql = 'SELECT COUNT(id) as count, author FROM poems GROUP BY author ORDER BY count DESC'
        result = db.execute(sql).fetchall()
    assert result != None 
    return render_template('showlist.html', rows=result)

@app.route("/showauthor", methods=['GET', 'POST'])
def call_showauthor():
    author = get_post_arg('author', 'Sova, Antonín', True)
    with get_db() as db:
        sql = 'SELECT id, title, book_id, body FROM poems WHERE author=?'
        poems = db.execute(sql, (author,)).fetchall()
        data = []
        for book_id, p in groupby(poems, lambda p: p[2]):
            book = db.execute('SELECT title, year FROM books WHERE id = ?', (book_id,)).fetchone()
            # TODO sort poems according to corpus_id
            data.append({'book': book, 'poems': list(p)})
    data.sort(key=lambda x: x['book'][1])
    return render_template('showauthor.html', author=author, rows=data)


# Adapted from THEaiTRE server
import base64
HASH_WIDTH_BYTES = sys.hash_info.width//8
from datetime import datetime
def text2id(text, add_timestamp=True):
    # hash
    # ! seed is not stable
    hash_bytes = hash(text).to_bytes(HASH_WIDTH_BYTES, 'big', signed=True)
    hash64 = base64.urlsafe_b64encode(hash_bytes).decode('ascii')[:-1]

    if add_timestamp:
        return datetime.now().strftime("%Y-%m-%d_%H-%M-%S_") + hash64
    else:
        return hash64

def poemdata2text(data):
    text = ''
    if data['author_name']:
        text += data['author_name'] + '\n'
    if data['title']:
        text += data['title'] + '\n'
    text += '\n'
    text += data['plaintext']
    
    return text

@app.route("/analyze", methods=['GET', 'POST'])
def call_analyze():
    text = get_post_arg('text', 'Matce pro kacířství syna vzali,\nna jesuitu jej vychovali;', True)
    output, k = okvetuj(text)
    poem_json = output[0]
    add_metadata_to_dict(poem_json)
    if poem_json['schools']:
        poem_json['schools'] = [poem_json['schools']]
    else:
        poem_json['schools'] = []
    
    if poem_json['id']:
        data = show_poem_html.show(poem_json, True)
        html = render_template('show_poem_html.html', **data)
        text = poemdata2text(data)
        return return_accepted_type(text, data, html)
    else:
        hash64 = text2id(text)
        poemid = f'{hash64}.json'
        with open(f'static/poemfiles/{poemid}', 'w') as outfile:
            json.dump(poem_json, outfile, ensure_ascii=False, indent=4)
        # TODO !!! this only works well for HTML but not for JSON or TEXT
        return redirect(EDUPO_SERVER_PATH + url_for('call_show', poemid=poemid))

@app.route("/genmotives", methods=['GET', 'POST'])
def call_genmotives():
    poemid = get_post_arg('poemid', None)
    text = get_post_arg('text', None)
    title = get_post_arg('title', None)
    assert poemid != None and text != None
    basne = 'básně'
    if title:
        basne = f'básně {title}'
    system = f"Jste literární vědec se zaměřením na poezii. Vaším úkolem je určit až 5 hlavních témat {basne}. Napište pouze tato témata, nic jiného, každé na samostatný řádek. Takto:\n 1. A\n 2. B\n 3. C"
    motives = generate_with_openai_simple(text, system)
    with open(f'static/genmotives/{poemid}.txt', 'w') as outfile:
        print(motives, file=outfile)
    return redirect(EDUPO_SERVER_PATH + url_for('call_show', poemid=poemid))

@app.route("/genimage", methods=['GET', 'POST'])
def call_genimage():
    poemid = get_post_arg('poemid', None)
    text = get_post_arg('text', None)
    title = get_post_arg('title', None)
    assert poemid != None and text != None
    if title:
        prompt = f"Vygeneruj obrázek '{title}', ilustrující toto: {text}"
    else:
        prompt = f"Vygeneruj obrázek, ilustrující toto: {text}"
    image_description = generate_image_with_openai(prompt, f'static/genimg/{poemid}.png')
    with open(f'static/genimg/{poemid}.txt', 'w') as outfile:
        print(image_description, file=outfile)
    return redirect(EDUPO_SERVER_PATH + url_for('call_show', poemid=poemid))
    # return show(poemid)

@app.route("/search", methods=['GET', 'POST'])
def call_search():
    # TODO do this nicely
    results = []
    query = get_post_arg('query', '')
    use_regex = get_post_arg('use_regex', False)
    with get_db() as db:
        if use_regex:
            # sql = f'SELECT id, title, author, regex_capture(captures, 0) as entire_match FROM poems WHERE body REGEXP ?'
            sql = f'SELECT id, title, author, body FROM poems WHERE body REGEXP ? LIMIT 20'
            poems = db.execute(sql, (query,)).fetchall()
            for poem in poems:
                results.append({
                    'id': poem["id"],
                    'author': poem["author"],
                    'title': poem["title"],
                    'body': poem["body"],
                    'match': re.findall(query.replace('"', "'"), str(poem['body']))
                    })
        else:
            sql = f'SELECT id, title, author, body FROM poems WHERE body LIKE ? LIMIT 20'
            poems = db.execute(sql, (f'%{query}%',)).fetchall()
            for poem in poems:
                results.append({
                    'id': poem["id"],
                    'author': poem["author"],
                    'title': poem["title"],
                    'body': poem["body"],
                    })
    return render_template('show_search_result.html', query=query, results=results)

@app.route("/openaigenerate", methods=['GET', 'POST'])
def call_generate_openai():
    prompt = get_post_arg('prompt', 'Máte rádi ptakopysky?')
    result = generate_with_openai_simple(prompt)
    return render_template('openaigenerate.html', prompt=prompt, result=result)

@app.route("/tajnejkill")
def kill():
    os._exit(0)

