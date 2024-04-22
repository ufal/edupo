#!/usr/bin/env python3
#coding: utf-8

from flask import Flask

app = Flask(__name__)
print(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/prdel")
def prdel_world():
    return "<p>Hello, Prdel!</p>"

