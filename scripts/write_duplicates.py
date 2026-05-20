import sqlite3
import json
import sys

duplicates = []
for filename in sys.argv[1:]:
    with open(filename) as f:
        duplicates += open(filename, 'r').read().splitlines()

duplicates = [x.split() for x in duplicates]

dupl = dict()
for f, g, _, d in duplicates:
    if float(d) > 0.66:
        dpls = set([f, g]) | dupl.get(f, set()) | dupl.get(g, set())
        dupl[f] = dpls
        dupl[g] = dpls

def num_lines(body):
    return sum(len(x) for x in body)

sqlite3.register_converter("json", json.loads)

with sqlite3.connect('new.db', detect_types=sqlite3.PARSE_DECLTYPES) as db:
    db.execute('BEGIN TRANSACTION;')
    #db.execute('UPDATE poems SET duplicate_tm=NULL;')

    visited = set()
    for d  in list(dupl.values()):
        id = '-'.join(sorted(d))
        if id in visited:
            continue
        visited.add(id)
        lst = db.execute('SELECT year, poems.id, poems.body FROM poems JOIN books ON poems.book_id=books.id WHERE poems.id IN ({})'.format(','.join(d)))
        lst = [(y if (y != 'neuveden') else 0, i, num_lines(b))  for y, i, b in lst]
        print(lst)
        lst.sort()
        kanonic = lst[-1][1]
        db.execute('UPDATE poems SET duplicate_tm={} WHERE id IN ({})'.format(kanonic, ','.join([str(id) for _, id, _ in lst[:-1]])))