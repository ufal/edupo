#!/usr/bin/env python3
#coding: utf-8

from flask import Flask, request, render_template, g, redirect, url_for, jsonify, Response, make_response
from flask_cors import CORS
import os
import requests
import json

app = Flask(__name__)
CORS(app)  # Povolit CORS pro všechny endpointy
print(__name__)

# I have not been able to persuade Flask that it is under / locally but under
# /edupo/ externally so this is a work-around
EDUPO_SERVER_PATH = os.getenv('EDUPO_SERVER_PATH', '')

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

def get_data(keys=[]):
    data = dict()
    for key in keys:
        data[key] = get_post_arg(key)
    return data

def redirect_for_poemid(poemid):
    return redirect(EDUPO_SERVER_PATH + url_for('call_show', poemid=poemid))

def store(data, poemid=None, datatype='poemfiles'):
    if datatype == 'poemfiles':
        assert data['plaintext'], "All JSON files must have plaintext filled in"
        if 'id' in data:
            poemid = data['id']
        else:
            poemid = text2id(data['plaintext'])
            data['id'] = poemid
        
        with open(f'static/poemfiles/{poemid}.json', 'w') as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=4)
        return poemid
    elif datatype == 'genimg':
        response = requests.get(f"{APIURL}/{data['url']}")
        with open(f'static/genimg/{poemid}.png', 'wb') as outfile:
            outfile.write(response.content)
        with open(f'static/genimg/{poemid}.txt', 'w') as outfile:
            print(data['description'], file=outfile)
    elif datatype == 'genmotives':
        with open(f'static/genmotives/{poemid}.txt', 'w') as outfile:
            print(data, file=outfile)
    elif datatype == 'gentts':
        response = requests.get(f"{APIURL}/{data['url']}")
        with open(f'static/gentts/{poemid}.mp3', 'wb') as outfile:
            outfile.write(response.content)
    else:
        assert False, f"Bad datatype: {datatype}"


### INTERFACE STARTS HERE ###

APIURL='http://localhost:5000/'
#APIURL='https://quest.ms.mff.cuni.cz/edupo-api/'
HEADERS_JSON = {"accept": "application/json"}
HEADERS_HTML = {"accept": "text/html"}
HEADERS_TXT = {"accept": "text/plain"}

# NOTE this is optimistic, has no error handling

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/prdel")
def prdel_world():
    response = requests.get(f"{APIURL}/prdel", headers=HEADERS_HTML)
    return response.text

@app.route("/input", methods=['GET', 'POST'])
def call_store():
    data = get_data(['text', 'title', 'author'])
    response = requests.get(f"{APIURL}/input", data, headers=HEADERS_JSON)
    poem = response.json()
    poemid = poem['id']
    store(poem)
    return redirect_for_poemid(poemid)

@app.route("/gen", methods=['GET', 'POST'])
def call_generuj():
    data = get_data(['rhyme_scheme', 'verses_count', 'syllables_count', 'metre', 'title', 'author'])
    data['first_words'] = get_post_arg('first_words', isarray=True, default=[])
    data['anaphors'] = get_post_arg('anaphors', isarray=True, default=[])
    data['epanastrophes'] = get_post_arg('epanastrophes', isarray=True, default=[])
    response = requests.get(f"{APIURL}/gen", data, headers=HEADERS_JSON)
    poem = response.json()
    poemid = poem['id']
    store(poem)
    return redirect_for_poemid(poemid)

def filename_if_exists(filename):
    if os.path.isfile(filename):
        return filename
    else:
        return None

def contents_if_exists(filename):
    if os.path.isfile(filename):
        with open(filename) as infile:
            return infile.read()
    else:
        return None

def ensure_qr_code(poemid):
    filename = f'static/qrcodes/{poemid}.png'
    if not os.path.isfile(filename):
        import qrcode
        base_url = 'https://quest.ms.mff.cuni.cz/edupo/show?poemid='
        url = f'{base_url}{poemid}'
        img = qrcode.make(url)
        img.save(filename)

@app.route("/show", methods=['GET', 'POST'])
def call_show():
    data = get_data(['poemid'])
    response = requests.get(f"{APIURL}/show", data, headers=HEADERS_JSON)
    poem = response.json()
    poemid = store(poem)
    
    poem['imgfile'] = filename_if_exists(
            f"static/genimg/{poemid}.png")
    poem['imgtitle'] = contents_if_exists(
            f"static/genimg/{poemid}.txt")
    poem['ttsfile'] = filename_if_exists(
            f"static/gentts/{poemid}.mp3")
    poem['motives'] = contents_if_exists(
            f"static/genmotives/{poemid}.txt")
    ensure_qr_code(poemid)
    
    # TODO could store poem again to ensure the above fields are filled in the
    # stored file (but we always fill them before showing so this is not
    # crucial)

    return render_template('show_poem_html.html', **poem)

@app.route("/showlist", methods=['GET', 'POST'])
def call_showlist():
    response = requests.get(f"{APIURL}/showlist", headers=HEADERS_JSON)
    data = response.json()
    return render_template('showlist.html', rows=data)

@app.route("/showlistgen", methods=['GET', 'POST'])
def call_showlistgen():
    response = requests.get(f"{APIURL}/showlistgen", headers=HEADERS_JSON)
    data = response.json()
    return render_template('showlistgen.html', poemids=data)

@app.route("/showauthor", methods=['GET', 'POST'])
def call_showauthor():
    data = get_data(['author'])
    response = requests.get(f"{APIURL}/showauthor", data, headers=HEADERS_HTML)
    return response.text
    # TODO json to tady zatim nevrací
    # data = response.json()
    # return render_template('showauthor.html', author=data['author'], rows=data['books'])

# can be called from input on main page -> no id
@app.route("/analyze", methods=['GET', 'POST'])
def call_analyze():
    data = get_data(['poemid', 'text', 'title', 'author'])
    # TODO send whole poem json
    response = requests.post(f"{APIURL}/analyze", data, headers=HEADERS_JSON)
    poem = response.json()
    poemid = poem['id']
    store(poem)
    return redirect_for_poemid(poemid)
    
@app.route("/genmotives", methods=['GET', 'POST'])
def call_genmotives():
    data = get_data(['poemid'])
    # TODO send whole poem json
    response = requests.get(f"{APIURL}/genmotives", data, headers=HEADERS_TXT)
    response.encoding='utf8'
    motives = response.text
    store(motives, poemid=data['poemid'], datatype='genmotives')
    return redirect_for_poemid(data['poemid'])

@app.route("/genimage", methods=['GET', 'POST'])
def call_genimage():
    data = get_data(['poemid'])
    # TODO send whole poem json
    response = requests.get(f"{APIURL}/genimage", data, headers=HEADERS_JSON)
    store(response.json(), poemid=data['poemid'], datatype='genimg')
    # TODO get and store binary data
    return redirect_for_poemid(data['poemid'])

@app.route("/gentts", methods=['GET', 'POST'])
def call_gentts():
    data = get_data(['poemid'])
    # TODO send whole poem json
    response = requests.get(f"{APIURL}/gentts", data, headers=HEADERS_JSON)
    store(response.json(), poemid=data['poemid'], datatype='gentts')
    # TODO get and store binary data
    return redirect_for_poemid(data['poemid'])

@app.route("/search", methods=['GET', 'POST'])
def call_search():
    data = get_data(['query', 'use_regex'])
    response = requests.get(f"{APIURL}/search", data, headers=HEADERS_JSON)
    results = response.json()
    return render_template('show_search_result.html', query=data['query'], results=results)
   
@app.route("/openaigenerate", methods=['GET', 'POST'])
def call_generate_openai():
    data = get_data(['prompt'])
    response = requests.get(f"{APIURL}/openaigenerate", data, headers=HEADERS_HTML)
    return response.text
    # TODO json to tady zatim nevrací
