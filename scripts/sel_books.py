#!/usr/bin/env python3
#coding: utf-8

import sys
import sqlite3
import requests
import json

import logging
logging.basicConfig(
    format='%(asctime)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO)

# DBFILE='/net/projects/EduPo/data/new.db'
DBFILE='/net/projects/EduPo/rur/new_withmood.db'

logging.info(DBFILE)

db = sqlite3.connect(DBFILE, detect_types=sqlite3.PARSE_DECLTYPES)
db.row_factory = sqlite3.Row
#db.enable_load_extension(True)
#db.load_extension("./regex0")

with open('../selected_authors.txt') as infile:
    for author in infile:
        author=author.strip()
        # print(f'\n=== {author} ===')
        print(f'    "{author}": [')
        sql = 'SELECT title FROM books WHERE author=?'
        result = db.execute(sql, (f'{author}',))
        for row in result.fetchall():
            # print(row[0])
            print(f'      "{row[0]}",')
        print('    ],')

