#!/usr/bin/env python3
#coding: utf-8

from flask import Flask, request
import os
from gen import generuj
from show_poem_html import show_file 

app = Flask(__name__)
print(__name__)

# TODO tohle se asi nemá dělat
# NOTE takhle pokud POSTuju tak se nedostanu k parametrum zadanym v URL; tj.
# nechceme dělat POST z formuláře kde by cílová URL obsahovala i GET parametry
# (to asi stejně nechceme)
def get_post_arg(key, default=None):
    if request.method == 'POST':
        return request.form.get(key, default)
    elif request.method == 'GET':
        return request.args.get(key, default)
    else:
        # TODO probably should not happen
        return default

@app.route("/")
def hello_world():
    return "<p>Vítejte v EduPo!</p>"

@app.route("/prdel")
def prdel_world():
    return "<p>Hello, Prdel!</p>"

@app.route("/gen", methods=['GET', 'POST'])
def call_generuj():
    rhyme_scheme = get_post_arg('rhyme_scheme', 'AABB')
    poet_start = rhyme_scheme
    verses = generuj(poet_start)
    return '<br>'.join(verses)

@app.route("/show")
def call_show(filename = '78468.json'):
    html = show_file(filename)
    return html

@app.route("/tajnejkill")
def kill():
    os._exit(0)

