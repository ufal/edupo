#!/usr/bin/env python3
#coding: utf-8

from flask import Flask, request, render_template, g
from itertools import groupby
import os
from gen import generuj
import show_poem_html
import sqlite3
import json
from collections import defaultdict
import re

import sys
sys.path.append("../kveta")
from kveta import okvetuj

app = Flask(__name__)
print(__name__)

DBFILE='/net/projects/EduPo/data/new.db'

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
def get_post_arg(key, default=None, nonempty=False):
    result = default
    if request.method == 'POST':
        result = request.form.get(key, default)
    elif request.method == 'GET':
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

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/prdel")
def prdel_world():
    return "<p>Hello, Prdel!</p>"

@app.route("/gen", methods=['GET', 'POST'])
def call_generuj():
    rhyme_scheme = get_post_arg('rhyme_scheme', 'AABB', True)
    metre = get_post_arg('metre')
    app.logger.info(f"Generate poem with scheme {rhyme_scheme}")
    poet_start = rhyme_scheme
    raw_output = generuj(poet_start, metre)
    clean_verses = raw_output[-len(rhyme_scheme)-1:]
    app.logger.info(f"Generated poem {clean_verses}")
    return render_template('show_poem_gen.html',
            clean_verses=clean_verses,
            raw='\n'.join(raw_output)
            )

@app.route("/show", methods=['GET', 'POST'])
def call_show():
    poemid = get_post_arg('poemid', '78468.json', True)
    if poemid.endswith('.json'):
        return show_poem_html.show_file(poemid)
    else:
        with get_db() as db:
            sql = 'SELECT *, books.title as b_title FROM poems, books, authors WHERE poems.id=? AND books.id=poems.book_id AND authors.identity=poems.author'
            result = db.execute(sql, (poemid,)).fetchone()
        assert result != None 
        html = show_poem_html.show(result)
        return html

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
        sql = 'SELECT id, title, book_id FROM poems WHERE author=?'
        poems = db.execute(sql, (author,)).fetchall()
        data = []
        for book_id, p in groupby(poems, lambda p: p[2]):
            book = db.execute('SELECT title, year FROM books WHERE id = ?', (book_id,)).fetchone()
            # TODO sort poems according to corpus_id
            data.append({'book': book, 'poems': list(p)})
    data.sort(key=lambda x: x['book'][1])
    return render_template('showauthor.html', author=author, rows=data)

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
    html = show_poem_html.show(poem_json, True)
    return html

@app.route("/search", methods=['GET', 'POST'])
def call_search():
    # TODO do this nicely
    results = []
    query = get_post_arg('query', '')
    use_regex = get_post_arg('use_regex', False)
    with get_db() as db:
        if use_regex:
            # sql = f'SELECT id, title, author, regex_capture(captures, 0) as entire_match FROM poems WHERE body REGEXP ?'
            sql = f'SELECT id, title, author, body FROM poems WHERE body REGEXP ?'
            poems = db.execute(sql, (query,)).fetchall()
            for poem in poems:
                results.append({
                    'id': poem["id"],
                    'author': poem["author"],
                    'title': poem["title"],
                    'match': re.findall(query.replace('"', "'"), str(poem['body']))
                    })
        else:
            sql = f'SELECT id, title, author FROM poems WHERE body LIKE ?'
            poems = db.execute(sql, (f'%{query}%',)).fetchall()
            for poem in poems:
                results.append({
                    'id': poem["id"],
                    'author': poem["author"],
                    'title': poem["title"],
                    })
    return render_template('show_search_result.html', query=query, results=results)

@app.route("/tajnejkill")
def kill():
    os._exit(0)

