#!/usr/bin/env python3
#coding: utf-8

import sys
sys.path.append("../kveta")
from kveta import okvetuj
from kveta import okvetuj_ccv


import sqlite3
import json

sqlite3.register_converter("json", json.loads)

DBFILE='/net/projects/EduPo/data/new.db'
# DBFILE='/net/projects/EduPo/data/new_copy.db'

def get_db():
    db = sqlite3.connect(DBFILE,
            detect_types=sqlite3.PARSE_DECLTYPES)
    db.row_factory = sqlite3.Row
    return db

if __name__=="__main__":
    try:
        poemid = int(sys.argv[1])
    except:
        poemid = 63470
    
    with get_db() as db:
        sql = 'SELECT *, books.title as b_title FROM poems, books, authors WHERE poems.id=? AND books.id=poems.book_id AND authors.identity=poems.author'
        result = db.execute(sql, (poemid,)).fetchone()
        assert result != None 
        # print(dict(result))
        # result obsahuje i metadata (autor. název, atd)
        # body už je ten JSON už jako DICT
        data = result['body']

    print("INPUT:")
    print(data)
    
    output = okvetuj_ccv(data)

    print("OUTPUT:")
    print(output)

    # a pak výhledově možná ještě TODO to uložit do databáze, ale to později

