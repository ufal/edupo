#!/usr/bin/env python3
#coding: utf-8

from flask import Flask, request, render_template, g, redirect, url_for, jsonify, Response, make_response, send_file
from flask_cors import CORS
from itertools import groupby
import os
# from gen import generuj, load_models
import show_poem_html
import sqlite3
import json
from collections import defaultdict
import re
import random
from openai_helper import *

import requests

import sys
sys.path.append("../kveta")
sys.path.append("../scripts/diphthongs")
from kveta import okvetuj, okvetuj_ccv
from get_measures import get_measures_from_analyzed_poem

app = Flask(__name__)
CORS(app)  # Povolit CORS pro všechny endpointy
print(__name__)

DBFILE='/net/projects/EduPo/data/new.db'

POEMFILES="static/poemfiles"

# I have not been able to persuade Flask that it is under / locally but under
# /edupo/ externally so this is a work-around
EDUPO_SERVER_PATH = os.getenv('EDUPO_SERVER_PATH', '')

MC_MODEL_PORT = os.getenv('MC_MODEL_PORT', 5010)
TM_MODEL_PORT = os.getenv('TM_MODEL_PORT', 5011)

sqlite3.register_converter("json", json.loads)

# load generator models
# load_models()

class ExceptionPoemDoesNotExist(Exception):
    pass

class ExceptionPoemInvalid(Exception):
    pass

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

# our defined order of priorities:
# 1. HTML (because of web browsers)
# 2. JSON (for APIs)
# 3. TEXT (fallback)
# the text can be text or URL; TODO maybe we should split and distinguish
# text/plain and text/uri-list
# the HTML can be HTML or redirect; TODO maybe redirects are stupid for API?
def get_accepted_type():
    # figure out what to return
    return_type = get_post_arg('accept')
    if return_type not in ['html', 'txt', 'json']:
        return_type = None
    if not return_type:
        if request.accept_mimetypes.accept_html:
            return_type = 'html'
        elif request.accept_mimetypes.accept_json:
            return_type = 'json'
        else:
            return_type = 'txt'
    return return_type

def return_error(text, exception, status=500):
    text = f"{text} Detaily o chybě: {exception}"
    json = '{"error": "' + text + '"}'
    return return_accepted_type(text, json, text, status=status)

def return_accepted_type(text, json, html, status=200):
    return_type = get_accepted_type()
    if return_type == 'html':
        if status == 200:
            return html
        else:
            return html, status
    elif return_type == 'json':
        if type(json) == str:
            # already JSON
            return Response(json, mimetype='application/json', status=status)
        else:
            return jsonify(json), status
    else:
        if return_type != 'txt':
            return f"Cannot return response of type {return_type}", 406
        if not text.endswith("\n"):
            text += "\n"
        return Response(text, mimetype='text/plain', status=status)

def redirect_for_poemid(poemid):
    return redirect(EDUPO_SERVER_PATH + url_for('call_show', poemid=poemid))

def return_accepted_type_for_poemid(data, html_template=None):
    """redirect for html unless html_template, poem2text_with_header for text"""
    
    if not 'id' in data:
        raise ExceptionPoemInvalid('id must be specified in data')

    return_type = get_accepted_type()
    if return_type == 'html':
        if html_template:
            return render_template(html_template, **data)
        else:
            return redirect_for_poemid(data['id'])
    elif return_type == 'json':
        return jsonify(data)
    else:
        if return_type != 'txt':
            return f"Cannot return response of type {return_type}", 406
        return Response(poem2text_with_header(data), mimetype='text/plain')

def poem2text(data):
    """Convert poem (loaded from JSON) to plaintext."""

    # the text itself
    if data['plaintext']:
        return data['plaintext']
    else:
        plaintext = list()
        prev_stanza_id = 0
        for verse in data['body']:
            stanza_id = verse.get("stanza", 0)
            if prev_stanza_id != stanza_id:
                plaintext.append('')
                prev_stanza_id = stanza_id
            plaintext.append(verse["text"])
        plaintext.append('')
        return '\n'.join(plaintext)

def poem2text_with_header(data, includeid=True):
    prefix = ''
    if includeid:
        prefix = f"{data['id']}\n\n"
    author = data['author_name'] if data['author_name'] else 'Anonym'
    title = data['title'] if data['title'] else 'Bez názvu'
    text = poem2text(data)
    if not text.endswith("\n"):
        text += "\n"
    
    return f"{prefix}{author}:\n{title}\n\n{text}"

import base64
HASH_WIDTH_BYTES = sys.hash_info.width//8
from datetime import datetime
def text2id(text, add_timestamp=True):
    """Generate ID based on text and timestamp"""
    # hash
    # ! seed is not stable
    hash_bytes = hash(text).to_bytes(HASH_WIDTH_BYTES, 'big', signed=True)
    hash64 = base64.urlsafe_b64encode(hash_bytes).decode('ascii')[:-1]

    if add_timestamp:
        return datetime.now().strftime("%Y-%m-%d_%H-%M-%S_") + hash64
    else:
        return hash64

def listgen():
    """
    List generated poem IDs
    """
    return [f for f in os.listdir(POEMFILES) if f.endswith('.json') and '_' in f]

# TODO do we need to run show_poem_html.show() always?
def get_poem_by_id(poemid=None, random_if_no_id=False):
    """If poemid is None, then get it from get/post arguments. If not set,
    rturn None OR take a random poem from db."""
    
    if poemid is None:
        poemid = get_post_arg('poemid')
        if not poemid:
            if random_if_no_id:
                poemid = str(random.randint(0,80229))
            else:
                return None

    if poemid == 'RANDOMGEN':
        poemids = listgen()
        poemid = random.choice(poemids)

    # check if path is allowed (do not allow traversing parent dirs)
    requested = os.path.abspath(f"{POEMFILES}/{poemid}")
    basedir = os.path.abspath(POEMFILES)
    path_allowed = (basedir == os.path.commonpath((basedir, requested)))

    if path_allowed and (os.path.isfile(f"{POEMFILES}/{poemid}.json") or os.path.isfile(f"{POEMFILES}/{poemid}")):
        # TODO always analyze ???
        #    kveta_result = okvetuj(data['plaintext'])
        #    data['body'] = kveta_result[0][0]['body']
        data = show_poem_html.show_file(poemid, POEMFILES)
        if 'plaintext' not in data:
            raise ExceptionPoemInvalid("All JSON files must have plaintext filled in")
    else:
        with get_db() as db:
            sql = 'SELECT *, books.title as b_title FROM poems, books, authors WHERE poems.id=? AND books.id=poems.book_id AND authors.identity=poems.author'
            result = db.execute(sql, (poemid,)).fetchone()
        if result == None:
            raise ExceptionPoemDoesNotExist("Poem with this id does not exist")
        result = dict(result)
        # always analyze
        result['body'] = okvetuj_ccv(result['body'])
        data = show_poem_html.show(result)
        data['plaintext'] = poem2text(data)
    
    return data

def get_data_tta():
    """Get text, title author"""
    data = {'plaintext': get_post_arg('text'),
            'title': get_post_arg('title', 'Bez názvu', True),
            'author_name': f"{get_post_arg('author', 'Anonym', True)} [vloženo uživatelem]",
            }
    
    if 'plaintext' not in data:
        raise ExceptionPoemInvalid("Text must not be empty!")
    
    return data

def store(data):
    if 'plaintext' not in data:
        raise ExceptionPoemInvalid("Text must not be empty!")
    
    if 'id' in data:
        poemid = data['id']
    else:
        poemid = text2id(data['plaintext'])
        data['id'] = poemid
    
    with open(f'static/poemfiles/{poemid}.json', 'w') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)
    
    return poemid


### INTERFACE STARTS HERE ###

@app.route("/")
@app.route("/index")
def hello_world():
    return render_template('index.html')

@app.route("/favicon.ico")
def favicon():
    return send_file('static/favicon.ico')

@app.route("/prdel", methods=['GET', 'POST'])
def prdel_world():
    # if request.method == "OPTIONS":
    #    response = make_response()
    #    response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
    #    response.headers.add("Access-Control-Allow-Methods", "GET, OPTIONS")
    #    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    #    response.headers.add("Access-Control-Allow-Credentials", "true")
    #    return response

    text = "Hello, Kyselá Prdel!"
    response = return_accepted_type(text, {'text': text}, f"<p>{text}</p>")
    # response = make_response(return_accepted_type(text, {'text': text}, f"<p>{text}</p>"))
    # response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
    # response.headers.add("Access-Control-Allow-Credentials", "true")
    
    # also can use a JSON string as json:
    # return return_accepted_type(text, "{'text': "+text+"}", f"<p>{text}</p>")
    return response

@app.route("/input", methods=['GET', 'POST'])
def call_store():
    data = get_data_tta()
    store(data)
    return return_accepted_type_for_poemid(data)

import zmq
def gen_zmq(params):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    if params['modelspec'] == 'tm':
        try:
            socket.connect(f"tcp://localhost:{TM_MODEL_PORT}")
        except:
            socket.connect(f"tcp://localhost:{MC_MODEL_PORT}")
    else:
        socket.connect(f"tcp://localhost:{MC_MODEL_PORT}")
    socket.send_string(json.dumps(params))
    return json.loads(socket.recv())

@app.route("/gen", methods=['GET', 'POST'])
def call_generuj():
    # empty or 'náhodně' means random
    params = dict()
    params['rhyme_scheme'] = get_post_arg('rhyme_scheme', '')
    params['verses_count'] = int(get_post_arg('verses_count', 0, True))
    params['syllables_count'] = int(get_post_arg('syllables_count', 0, True))
    params['metre'] = get_post_arg('metre')
    params['first_words'] = [word.strip() for word in get_post_arg('first_words', isarray=True, default=[])]
    # TODO if all first_words are empty then ignore
    params['anaphors'] = [int(x) for x in get_post_arg('anaphors', isarray=True, default=[])]
    params['epanastrophes'] = [int(x) for x in get_post_arg('epanastrophes', isarray=True, default=[])]
    params['temperature'] = float(get_post_arg('temperature', '1'))
    params['max_strophes'] = int(get_post_arg('max_strophes', '2'))
    params['title'] = get_post_arg('title', 'Bez názvu')
    params['author_name'] = get_post_arg('author', 'Anonym')
    params['modelspec'] = get_post_arg('modelspec', 'mc')
    
    geninput = (f"Generate poem with parameters: {params}")
    app.logger.info(geninput)
    # raw_output, clean_verses, author_name, title = generuj(dict(params))
    raw_output, clean_verses, author_name, title = gen_zmq(params)
    app.logger.info(f"Generated poem {clean_verses}")
  
    # sets must be lists now
    params['anaphors'] = list(params['anaphors'])
    params['epanastrophes'] = list(params['epanastrophes'])

    data = {
            'geninput': params,
            'plaintext': "\n".join(clean_verses),
            'rawtext': raw_output,
            'title': title,
            'author_name': f"{author_name} [vygenerováno]",
            }
    store(data)
    
    return return_accepted_type_for_poemid(data)

METRENAMES = {
    'T': 'trochej',
    'J': 'jamb',
    'D': 'daktyl',
    'N': 'volný',
}

@app.route("/geninter", methods=['GET', 'POST'])
def call_generuj_interaktivne():
    
    params = dict()
    
    # generation settings
    params['interactive_mode'] = get_post_arg('interactive_mode', 'lines_gh', True)
    params['modelspec'] = get_post_arg('modelspec', 'mc', True)
    params['title'] = get_post_arg('title', 'Bez názvu', True)
    params['metre'] = get_post_arg('metre', 'T', True)
    params['rhyme_scheme'] = get_post_arg('rhyme_scheme', 'AABB', True)
    params['syllables_count'] = int(get_post_arg('syllables_count', 8, True))
    
    # generation process
    poemid = get_post_arg('poemid')
    if poemid:
        params['id'] = poemid
    params['rawtext'] = get_post_arg('rawtext', '')
    params['userinput'] = get_post_arg('userinput', '')

    app.logger.info(f"Generate interactively poem with parameters: {params}")
    if params['rawtext'] or params['userinput'] or params['interactive_mode'].endswith('gh'):
        raw_output, clean_verses, author_name, title = gen_zmq(params)
        app.logger.info(f"Generated interatively part of poem: {clean_verses}")
        # TODO store author_name, title
    else:
        # user starts, nothing to generate yet
        raw_output, clean_verses = '', []
    
    # TODO if the poem is already a full quatrain, handle that
  
    data = {
            **params,
            'geninput': params,
            'plaintext': "\n".join(clean_verses),
            'rawtext': raw_output,
            'metrum': METRENAMES[params['metre']],
            }
    data['poemid'] = store(data)
    
    if '<|endoftext|>' in raw_output:
        return return_accepted_type(raw_output, data, redirect_for_poemid(poemid))
    else:
        html = render_template('interactive_gen_process.html', **data)
        return return_accepted_type(raw_output, data, html)

@app.route("/show", methods=['GET', 'POST'])
def call_show():
    data = get_poem_by_id(random_if_no_id=True)
    if data:
        return return_accepted_type_for_poemid(data, 'show_poem_html.html')
    else:
        return return_error('The requested poem does not exist.', get_post_arg('poemid'), 404)

@app.route("/showlist", methods=['GET', 'POST'])
def call_showlist():
    with get_db() as db:
        sql = 'SELECT COUNT(id) as count, author FROM poems GROUP BY author ORDER BY count DESC'
        result = db.execute(sql).fetchall()
    assert result != None, "Database result is empty"
    html = render_template('showlist.html', rows=result)
    text = "\n".join([f"{row['count']}x {row['author']}" for row in result])
    data = [dict(row) for row in result]
    return return_accepted_type(text, data, html)

@app.route("/showlistgen", methods=['GET', 'POST'])
def call_showlistgen():
    poemids = listgen()
    poemids.sort(reverse=True)
    html = render_template('showlistgen.html', poemids=poemids)
    text = "\n".join(poemids)
    return return_accepted_type(text, poemids, html)

@app.route("/showauthor", methods=['GET', 'POST'])
def call_showauthor():
    author = get_post_arg('author', 'Sova, Antonín', True)
    text = [author]
    with get_db() as db:
        sql = 'SELECT id, title, book_id, body FROM poems WHERE author=?'
        poems = db.execute(sql, (author,)).fetchall()
        data = []
        text.append("SBÍRKY:")
        for book_id, p in groupby(poems, lambda p: p[2]):
            book = db.execute('SELECT title, year FROM books WHERE id = ?', (book_id,)).fetchone()
            # TODO sort poems according to corpus_id
            data.append({'book': book, 'poems': list(p)})
            text.append(f"{book['title'], book['year']}")
        text.append("BÁSNĚ:")
        text.extend([f"{poem['id']}: {poem['title']}" for poem in poems])
    data.sort(key=lambda x: x['book'][1])
    html = render_template('showauthor.html', author=author, rows=data)
    
    # TODO JSON to nevrací
    return return_accepted_type("\n".join(text), {'author': author, 'books': data}, html)

# can be called from input on main page -> no id
@app.route("/analyze", methods=['GET', 'POST'])
def call_analyze():
    data = get_poem_by_id()
    if data is None:
        data = get_data_tta()
    
    if not data.get('plaintext', ''):
        raise ExceptionPoemInvalid("Text must not be empty!")
    
    if 'body' in data:
        kveta_result = okvetuj_ccv(data['body'])
        data['body'] = [kveta_result]
    else:
        kveta_result = okvetuj(data['plaintext'])
        data['body'] = kveta_result[0][0]['body']
        # metrics
        data['measures'] = get_measures_from_analyzed_poem(data['body'])

    store(data)

    return return_accepted_type_for_poemid(data)

@app.route("/genmotives", methods=['GET', 'POST'])
def call_genmotives():
    poemid = get_post_arg('poemid')
    data = get_poem_by_id(poemid)
    
    basne = 'básně'
    if data['title'] and not 'Bez názvu' in data['title']:
        basne = f"básně {data['title']}"
    system = f"Jste literární vědec se zaměřením na poezii. Vaším úkolem je určit až 5 hlavních témat {basne}. Napište pouze tato témata, nic jiného, každé na samostatný řádek. Takto:\n 1. A\n 2. B\n 3. C"
    
    motives = generate_with_openai_simple(poem2text(data), system)
    
    with open(f'static/genmotives/{poemid}.txt', 'w') as outfile:
        print(motives, file=outfile)
    
    return return_accepted_type(motives,
            {'motives': motives.split("\n")},
            redirect_for_poemid(poemid)
            )

@app.route("/processopenai", methods=['GET', 'POST'])
def call_processopenai():
    poemid = get_post_arg('poemid')
    data = get_poem_by_id(poemid)
    
    if not 'openai' in data:
        data['openai'] = []

    
    prompt = get_post_arg('openaiprompt')
    output = generate_with_openai_simple(poem2text_with_header(data, False), prompt)
    data['openai'].append({'prompt': prompt, 'output': output})
    store(data)
    
    return return_accepted_type(
            data['openai'][-1]['output'],
            data['openai'][-1],
            redirect_for_poemid(poemid)
            )

@app.route("/translate", methods=['GET', 'POST'])
def call_translate():
    poemid = get_post_arg('poemid')
    data = get_poem_by_id(poemid)
    
    if not 'translations' in data:
        data['translations'] = {}
    
    language = get_post_arg('language', 'sk')

    if language == 'sk':
        response = requests.post(
            'https://lindat.mff.cuni.cz/services/rest/cesilko/translate',
            data={'data': poem2text(data)}
            )
        response.raise_for_status()
        response.encoding='utf8'
        data['translations']['sk'] = response.json()['result']
    else:
        response = requests.post(
            'http://lindat.mff.cuni.cz/services/translation/api/v2/models/cs-uk',
            data={'input_text': poem2text(data)},
            headers={"accept": "text/plain"}
            )
        response.raise_for_status()
        response.encoding='utf8'
        data['translations'][language] = response.text

    store(data)
    
    return return_accepted_type(
            data['translations'][language],
            data['translations'][language],
            redirect_for_poemid(poemid)
            )

@app.route("/genimage", methods=['GET', 'POST'])
def call_genimage():
    poemid = get_post_arg('poemid')
    data = get_poem_by_id(poemid)
    if data['title'] and not 'Bez názvu' in data['title']:
        prompt = f"Vygeneruj obrázek '{data['title']}', ilustrující toto: {poem2text(data)}"
    else:
        prompt = f"Vygeneruj obrázek, ilustrující toto: {poem2text(data)}"
    
    image_description = generate_image_with_openai(prompt, f'static/genimg/{poemid}.png')
    
    with open(f'static/genimg/{poemid}.txt', 'w') as outfile:
        print(image_description, file=outfile)
    
    url = url_for('static', filename=f'genimg/{poemid}.png')
    return return_accepted_type(url,
            {'url': url, 'description': image_description},
            redirect_for_poemid(poemid)
            )

from gtts import gTTS
@app.route("/gentts", methods=['GET', 'POST'])
def call_gentts():
    poemid = get_post_arg('poemid')
    data = get_poem_by_id(poemid)
    filename = f'static/gentts/{poemid}.mp3'
    text = poem2text_with_header(data, includeid=False)
    tts = gTTS(text, lang='cs', tld='cz', slow=True)
    tts.save(filename)
    
    url = url_for('static', filename=f'gentts/{poemid}.mp3')
    return return_accepted_type(url,
            {'url': url},
            redirect_for_poemid(poemid)
            )

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
    html = render_template('show_search_result.html', query=query, results=results)
    text = "\n".join([f"{result['id']} ({result['author']}: {result['title']})" for result in results])
    return return_accepted_type(text, results, html)

@app.route("/openaigenerate", methods=['GET', 'POST'])
def call_generate_openai():
    prompt = get_post_arg('prompt', 'Máte rádi ptakopysky?')
    result = generate_with_openai_simple(prompt)
    return render_template('openaigenerate.html', prompt=prompt, result=result)

@app.route("/logs", methods=['GET', 'POST'])
def call_logs():
    n = int(get_post_arg('n', '20'))
    backlog = sorted([f for f in os.listdir('logs') if f.startswith('app.')])[-1]
    frontlog = sorted([f for f in os.listdir('../frontend/logs') if f.endswith('.log')])[-1]
    filenames = ['../autodeploy.log', f"../frontend/logs/{frontlog}", f"../backend/logs/{backlog}", f"../backend/logs/gen_mc.log", f"../backend/logs/gen_tm.log"]

    result = list()
    for filename in filenames:
        with open(filename) as infile:
            result.append(f'==== {filename} ====\n')
            lines = infile.readlines()
            result.extend(lines[-n:])
            result.append('\n\n')

    text = ''.join(result)
    html = f"<pre>{text}</pre>"

    return return_accepted_type(text, result, html)

@app.errorhandler(ExceptionPoemInvalid)
def handle_exception(e):
    app.logger.exception('EXCEPTION')
    return return_error("Báseň nemá správný formát, např. neobsahuje žádný text.", e, 422)

@app.errorhandler(ExceptionPoemDoesNotExist)
def handle_exception(e):
    app.logger.exception('EXCEPTION')
    return return_error("Požadovaná báseň neexistuje.", e, 404)

@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.exception('EXCEPTION')
    return return_error("Došlo k chybě. Můžete to zkusit znova.", e)
