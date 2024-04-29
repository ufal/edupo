import sqlite3
import json
import time

cas = time.time()
print('Reading original database.', end=' ')
db = sqlite3.connect('../data/KCV_komplet/cs.db')
cur = db.cursor()
jsons = cur.execute("select p_object from main;").fetchall()
db.close()
print('Done in {:.2f} s.'.format(time.time() - cas))

cas = time.time()
print('Converting JSONs.', end=' ')
jsons = [json.loads(j[0]) for j in jsons]
print('Done in {:.2f} s.'.format(time.time() - cas))

print('Creating authors table.', end=' ')
# get authors
authors = [j['p_author'] for j in jsons] + [j['b_author'] for j in jsons]
a_dict = {}
for a in authors:
    if a['identity'] in a_dict:
        assert a_dict[a['identity']]['born'] == a['born']
        assert a_dict[a['identity']]['died'] == a['died']
        # if a_dict[a['identity']]['name'] != a['name']: print(a_dict[a['identity']]['name'], '|', a['name'])
    else:
        a_dict[a['identity']] = a
print('Done.')

print('Creating books table.', end=' ')
# get authors
b_dict = {}
for b in jsons:
    id = int(b['book_id'])
    if id in b_dict:
        for k in b['biblio']:
            if k == 'p_title':
                continue
            assert b_dict[id][k] == b['biblio'][k], (id, k, b_dict[id][k], b['biblio'][k])
        assert b_dict[id]['author'] == b['b_author']['identity']
    b_dict[id] = dict()
    b_dict[id]['id'] = id
    for k in b['biblio']:
        if k == 'p_title':
                continue
        b_dict[id][k] = b['biblio'][k]
    b_dict[id]['author'] = b['b_author']['identity']
print('Done.')

print('Creating new database.', end=' ')
con = sqlite3.connect("new.db")
cur = con.cursor()
cur.execute("CREATE TABLE authors (identity STRING, born YEAR, died YEAR, PRIMARY KEY (identity));")
for a in a_dict.values():
    cur.execute("INSERT INTO authors VALUES (?, ?, ?);", (a['identity'], a['born'], a['died']))
cur.execute("CREATE TABLE books (id INT, title STRING, subtitle STRING, author STRING, motto STRING, motto_aut STRING," + \
            " publisher STRING, edition STRING, place STRING, dedication STRING, pages STRING, year YEAR, signature STRING, PRIMARY KEY (id));")
for b in b_dict.values():
    cur.execute("INSERT INTO books VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
                (b['id'], b['b_title'], b['b_subtitle'], b['author'], b['motto'], b['motto_aut'], b['publisher'], b['edition'],
                 b['place'], b['dedication'], b['pages'], b['year'], b['signature']))
con.commit()
print('Done.')

# get books

cur.close()
