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


sql = 'SELECT rowid FROM poems WHERE id IS NULL'
result = db.execute(sql)

newid = 100000

cur = db.cursor()
for row in result.fetchall():
    rowid = row['rowid'] 
    cur.execute("UPDATE poems SET id = ? WHERE rowid = ?", (newid, rowid))
    #print(f"set {rowid} to {newid}")
    newid += 1
    if newid % 1000 == 0:
        print(newid)
        db.commit()


db.commit()
db.close()
