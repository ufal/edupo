#!/usr/bin/env python3
#coding: utf-8

import sys
import sqlite3
import requests

sys.path.append("../backend")
from app import guessmood

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

ids = range(5,8)


for poemid in ids:
    logging.debug(poemid)

    sql = 'SELECT title, body FROM poems WHERE poems.id=?'
    result = db.execute(sql, (poemid,)).fetchone()
    data = dict(result)

    logging.debug(data['title'])
    
    mood = guessmood(data)

    logging.debug(mood)
    
    logging.info(f"{poemid} {data['title']}: {mood}")

    # TODO store to DB

