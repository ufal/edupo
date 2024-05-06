#!/usr/bin/env python3
#coding: utf-8

from flask import Flask, request, render_template, g
import os
from gen import generuj
import show_poem_html
import sqlite3
import json
from collections import defaultdict

app = Flask(__name__)
print(__name__)

DBFILE='/net/projects/EduPo/data/new.db'
#DBFILE='/net/projects/EduPo/data/new_copy.db'

sqlite3.register_converter("json", json.loads)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DBFILE,
                detect_types=sqlite3.PARSE_DECLTYPES)
        db.row_factory = sqlite3.Row
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

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/prdel")
def prdel_world():
    return "<p>Hello, Prdel!</p>"

@app.route("/gen", methods=['GET', 'POST'])
def call_generuj():
    rhyme_scheme = get_post_arg('rhyme_scheme', 'AABB', True)
    app.logger.info(f"Generate poem with scheme {rhyme_scheme}")
    poet_start = rhyme_scheme
    verses = generuj(poet_start)
    clean_verses = verses[-len(rhyme_scheme)-1:]
    app.logger.info(f"Generated poem {clean_verses}")
    return '<br>'.join(verses)

@app.route("/show", methods=['GET', 'POST'])
def call_show():
    poemid = get_post_arg('poemid', '78468.json', True)
    if poemid.endswith('.json'):
        return show_poem_html.show_file(poemid)
    else:
        table = get_post_arg('table', 'poems', True)
        with get_db() as db:
            sql = f'SELECT * FROM {table} WHERE id={poemid}'
            result = db.execute(sql).fetchone()
        assert result != None 
        html = show_poem_html.show(result)
        return html

@app.route("/tajnejkill")
def kill():
    os._exit(0)

