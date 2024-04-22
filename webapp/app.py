#!/usr/bin/env python3
#coding: utf-8

from flask import Flask
import os

app = Flask(__name__)
print(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/prdel")
def prdel_world():
    return "<p>Hello, Prdel!</p>"

@app.route("/tajnejkill")
def kill():
    os._exit(0)

