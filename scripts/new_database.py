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
    b_dict[id]['author_name'] = b['b_author']['name']
print('Done.')

print('Creating poems table.', end=' ')
p_dict = {}
for id, b in enumerate(jsons):
    p_dict[id] = dict()
    p_dict[id]['id'] = id
    book_id = int(b['book_id'])
    assert book_id in b_dict
    p_dict[id]['book_id'] = book_id
    p_dict[id]['author'] = b['p_author']['identity']
    p_dict[id]['author_name'] = b['p_author']['name']
    p_dict[id]['schools'] = b['schools']
    p_dict[id]['title'] = b['biblio']['p_title']
    p_dict[id]['poem_id_corp'] = b['poem_id']
    p_dict[id]['schemes'] = b['schemes']
    p_dict[id]['body'] = b['body']
print('Done.')

print('Creating new database.', end=' ')
con = sqlite3.connect("new.db")
cur = con.cursor()
cur.execute("CREATE TABLE authors (identity STRING PRIMARY KEY, born YEAR, died YEAR);")
for a in a_dict.values():
    cur.execute("INSERT INTO authors VALUES (?, ?, ?);", (a['identity'], a['born'], a['died']))
cur.execute("CREATE TABLE books (id INT PRIMARY KEY, title STRING, subtitle STRING, author STRING REFERENCES authors(identity)," + \
            " author_name STRING, motto STRING, motto_aut STRING," + \
            " publisher STRING, edition STRING, place STRING, dedication STRING, pages STRING, year YEAR, signature STRING);")
for b in b_dict.values():
    cur.execute("INSERT INTO books VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
                (b['id'], b['b_title'], b['b_subtitle'], b['author'], b['author_name'], b['motto'], b['motto_aut'], b['publisher'], b['edition'],
                 b['place'], b['dedication'], b['pages'], b['year'], b['signature']))
cur.execute("CREATE TABLE poems (id INT PRIMARY KEY, book_id INT REFERENCES books(id), author STRING REFERENCES authors(identity)," + \
            " author_name STRING, title STRING, poem_id_corp STRING," + \
            " schools JSON, schemes JSON, body JSON, duplicate_plechac INT REFERENCES poems(id), duplicate_tm INT REFERENCES poems(id));")
for p in p_dict.values():
    cur.execute("INSERT INTO poems VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
                (p['id'], p['book_id'], p['author'], p['author_name'], p['title'], p['poem_id_corp'],
                 json.dumps(p['schools']), json.dumps(p['schemes']), json.dumps(p['body']),
                 None, None))
con.commit()
print('Done.')

print('Fixing bugs in the data.', end=' ')

cur.execute('UPDATE books SET year=1876 WHERE id=1264;')
con.commit()

print('Done.')

cur.close()
con.close()
