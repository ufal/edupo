import sqlite3
import json
import sys
from collections import Counter

sqlite3.register_converter("json", json.loads)

with sqlite3.connect('new.db', detect_types=sqlite3.PARSE_DECLTYPES) as db:
    poems = db.execute('SELECT id, body, author FROM poems;')

def format_m(lst):
    return '/'.join(sorted(lst))

authors = dict()
for id, body, author in poems:
    lst = [format_m([list(z.keys())[0] for z in y['metre']]) for x in body for y in x]
    metra = set(lst)
    if sys.argv[1] == 'poem':
        if len(metra) > 1:
            print(id, list(metra), Counter(lst))
    elif sys.argv[1] == 'verse':
        for x in metra:
            if '/' in x:
                print(id, list(metra))
    elif sys.argv[1] == 'amfi':
        for x in metra:
            if 'A' in x:
                print(id, list(metra), author)
                authors[author] = authors.get(author, 0) + 1
if sys.argv[1] == 'amfi' and len(sys.argv) > 2 and sys.argv[2] == 'authors':
    for a, c in sorted(authors.items(), key=lambda x: x[1], reverse=True):
        print(a, c)