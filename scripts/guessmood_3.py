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



ids = range(1,160360)
#ids = range(1,20)


for rowid in ids:
    logging.info(f"ROWID {rowid}")

    sql = 'SELECT id, title, body, mood FROM poems WHERE rowid=?'
    result = db.execute(sql, (rowid,)).fetchone()
    data = dict(result)
    logging.debug(data['title'])

    if data['mood']:
        logging.info(f"UŽ JE: {data['title']}: {data['mood']}")
    else:
        mood = guessmood(data)
        logging.debug(mood)
        # store to DB
        sql = "UPDATE poems SET mood = ? WHERE rowid=?"
        result = db.execute(sql, (mood,rowid) )
        logging.debug(result)
        
        logging.info(f"{data['id']} {data['title']}: {mood}")

logging.info('Commit and close')
db.commit()
db.close()
logging.info('Done')
