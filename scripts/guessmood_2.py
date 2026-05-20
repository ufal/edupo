#!/usr/bin/env python3
#coding: utf-8

import sys
import sqlite3
import requests
import json

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

# add column 'mood'
cur = db.cursor()
cur.execute("PRAGMA table_info(poems)")
columns = {row[1] for row in cur.fetchall()}

if "mood" not in columns:
    logging.info("Přidávám sloupec")
    cur.execute("""
        ALTER TABLE poems
        ADD COLUMN mood
    """)
    db.commit()
else:
    logging.info("Sloupec už je")



ids = range(5,10)


for poemid in ids:
    logging.debug(poemid)

    sql = 'SELECT title, body, mood FROM poems WHERE poems.id=?'
    result = db.execute(sql, (poemid,)).fetchone()
    data = dict(result)
    logging.debug(data['title'])

    if data['mood']:
        logging.info(f"UŽ JE: {poemid} {data['title']}: {data['mood']}")
    else:
        mood = guessmood(data)
        logging.debug(mood)
        # store to DB
        data['mood'] = mood
        #sql = 'UPDATE poems SET body=? WHERE poems.id=?'
        #result = db.execute(sql, (json.dumps(data, ensure_ascii=False),poemid))
        # sql = "UPDATE poems SET body = json_set(body, '$.mood', ?) WHERE poems.id=?"
        # result = db.execute(sql, (mood,poemid) )
        sql = "UPDATE poems SET mood = ? WHERE poems.id=?"
        result = db.execute(sql, (mood,poemid) )
        logging.debug(result)
        
        logging.info(f"{poemid} {data['title']}: {mood}")

logging.info('Commit and close')
db.commit()
db.close()
logging.info('Done')
