import sqlite3
import json

sqlite3.register_converter("json", json.loads)

with sqlite3.connect('new.db', detect_types=sqlite3.PARSE_DECLTYPES) as db:
    poems = db.execute('SELECT id, body FROM poems;')

for id, body in poems:
    metra = set([list(z.keys())[0] for x in body for y in x for z in y['metre']])
    if len(metra) > 1:
        print(id, list(metra))