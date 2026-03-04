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


from collections import Counter

motives_freq = Counter()

sql = 'SELECT motives FROM poems'
result = db.execute(sql)
for row in result.fetchall():
    motives = json.loads(row['motives'])
    for m in motives:
        motives_freq[m] += 1 

for motiv, pocet in motives_freq.most_common(1000):
    print(f"{pocet}x {motiv}")

