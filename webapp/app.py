#!/usr/bin/env python3
#coding: utf-8

from flask import Flask
import os
from gen import generuj
from show_poem_html import show_file 

app = Flask(__name__)
print(__name__)

@app.route("/")
def hello_world():
    return "<p>Vítejte v EduPo!</p>"

@app.route("/prdel")
def prdel_world():
    return "<p>Hello, Prdel!</p>"

@app.route("/gen")
def call_generuj(poet_start = 'AABB'):
    verses = generuj(poet_start)
    return '<br>'.join(verses)

@app.route("/show")
def call_show(filename = '78468.json'):
    html = show_file(filename)
    return html

@app.route("/tajnejkill")
def kill():
    os._exit(0)

