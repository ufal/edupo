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

scores = {}
for f, g, _, d in duplicates:
    scores[(f, g)] = float(d)

sqlite3.register_converter("json", json.loads)
db = sqlite3.connect('new.db', detect_types=sqlite3.PARSE_DECLTYPES)
cur = db.cursor()

cur.execute('UPDATE poems SET duplicate_tm=NULL')

visited = set()
for d  in list(dupl.values()):
    id = '-'.join(sorted(d))
    if id in visited:
        continue
    visited.add(id)
    lst = cur.execute('SELECT year, poems.id FROM poems JOIN books ON poems.book_id=books.id WHERE poems.id IN ({})'.format(','.join(d))).fetchall()
    lst = [(y, i) if (y != 'neuveden') else (0, i) for y, i in lst]
    print(lst)
    lst.sort()
    kanonic = lst[-1][1]
    cur.execute('UPDATE poems SET duplicate_tm={} WHERE id IN ({})'.format(kanonic, ','.join([str(id) for _, id in lst[:-1]])))
db.commit()
db.close()