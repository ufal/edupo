#!/usr/bin/env python3
#coding: utf-8

import sys
import sqlite3
import requests
import json

sys.path.append("../backend")

import logging
logging.basicConfig(
    format='%(asctime)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO)

DBFILE='/net/projects/EduPo/data/new.db'
# DBFILE='/net/projects/EduPo/rur/new_withmood.db'

logging.info(DBFILE)

db = sqlite3.connect(DBFILE, detect_types=sqlite3.PARSE_DECLTYPES)
db.row_factory = sqlite3.Row
#db.enable_load_extension(True)
#db.load_extension("./regex0")

# dict: form -> author -> sbírka -> báseň 
# result[sonet][vrchlický][výběr] = {id: 123, title: 'sdafasdf'}
result = dict()

#ids = range(1,160360)
ids = range(1000)
ids = range(80229)

logging.info('Reading')
for poemid in ids:
    if poemid % 1000 == 0:
        logging.info(poemid)
    sql = 'SELECT *, books.title as b_title FROM poems, books, authors WHERE poems.id=? AND books.id=poems.book_id AND authors.identity=poems.author'
    sql_result = db.execute(sql, (poemid,)).fetchone()
    data = dict(sql_result)
    data['title'] = str(data['title'])
    if type(data['schemes']) == str:
        data['schemes'] = json.loads(data['schemes'])

    form = data['schemes'].get('form', None)
    if form:
        # print(poemid, data['author'], data['b_title'], data['title'], form)
        if form not in result:
            result[form] = dict()
        if data['author'] not in result[form]:
            result[form][data['author']] = dict()
        if data['b_title'] not in result[form][data['author']]:
            result[form][data['author']][data['b_title']] = list()
        result[form][data['author']][data['b_title']].append(
                {'id': poemid, 'title': data['title']})
logging.info('Done reading')

logging.info('Writing')

# header
print('''
<style>
h1 {
  position: sticky;
  top: 0;
  background: yellow;
  padding: 1ex;
}
</style>
''')

# TOC
print(f'<ul>')
for form in result:
    print(f'<li><a href="#{form}">{form}</a></li>')
print(f'</ul><hr>')

# lists
for form in result:
    logging.info(form)
    print(f'<h1 id="{form}">{form}</h1>')
    for author in result[form]:
        print(f'<h2>{author}</h2>')
        for book in result[form][author]:
            print(f'<h3>{book}</h3><ol>')
            for poem in result[form][author][book]:
                print(f'<li value="{poem["id"]}"><a href="https://quest.ms.mff.cuni.cz/edupo-api/show?poemid={poem["id"]}">{poem["title"]}</a></li>')
            print('</ol>')
    print(f'<hr>')


logging.info('Done')
