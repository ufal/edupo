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


# add column 'simplemotives'
cur = db.cursor()
cur.execute("PRAGMA table_info(poems)")
columns = {row[1] for row in cur.fetchall()}

if "simplemotives" not in columns:
    logging.info("Přidávám sloupec")
    cur.execute("""
        ALTER TABLE poems
        ADD COLUMN simplemotives
    """)
    db.commit()
else:
    logging.info("Sloupec už je")


sys.path.append("../backend")
from openai_helper import generate_with_openai_simple
        
system = f"Jsi literární vědec, zpracováváš seznamy motivů v básních. Popisy motivů jsou ale příliš komplexní, potřebujeme je zjednodušit, tak aby motivem vždy bylo ideálně jedno jednoduché podstatné jméno, případně krátká fráze.  Motivy by rozhodně neměly obsahovat spojku 'a'. Pro motiv, který dostaneš na vstupu, vypiš jeden nebo několik jednodušších motivů. Například pro 'Příroda a její cykly' a vypiš 'příroda' a 'cykly přírody'; pro 'Rodinné vztahy' vypiš 'rodina' a vztahy'; pro 'Pomíjivost času' vypiš 'pomíjivost času' a 'čas'; pro 'Příroda a její obnova' vypiš 'příroda' a 'obnova přírody'; pro 'Kulturní a rasové rozdíly' vypiš 'kulturní rozdíly' a 'rasové rozdíly'; pro 'Vztah mezi lidmi a přírodou' vypiš jen 'lidé' a 'příroda'; 'Krása a její vnímání' vypiš 'krása' a 'vnímání krásy'.  Vypiš pouze zjednodušené motivy, každý na jeden řádek. Nic jiného na výstup nevypisuj."

def simplify(motive):
    # X a Y
    words = motive.lower().split()
    if len(words) == 3 and words[1] == 'a':
        return words[0], words[2]
    elif len(words) == 1:
        return (words[0], )
    else:
        sm = generate_with_openai_simple(motive, system) 
        return [m.strip() for m in sm.split('\n')]


from collections import Counter

sql = 'SELECT motives FROM poems LIMIT 100'
result = db.execute(sql)
for row in result.fetchall():
    #try:
        motives = json.loads(row['motives'])
        for m in motives:
            ms = simplify(m)
            print(m, '->', ms)
    #except:
    #    print(row['motives'], file=sys.stderr)


