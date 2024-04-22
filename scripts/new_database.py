import sqlite3
import json

print('Reading original database.', end=' ')
db = sqlite3.connect('../data/KCV_komplet/cs.db')
cur = db.cursor()
jsons = cur.execute("select p_object from main;").fetchall()
db.close()
print('Done.')

print('Converting JSONs.', end=' ')
jsons = [json.loads(j[0]) for j in jsons]
print('Done.')

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

print('Creating new database.', end=' ')
con = sqlite3.connect("new.db")
cur = con.cursor()
cur.execute("CREATE TABLE authors (identity TEXT, born YEAR, died YEAR, PRIMARY KEY (identity));")
for a in a_dict.values():
    cur.execute("INSERT INTO authors VALUES (?, ?, ?);", (a['identity'], a['born'], a['died']))
con.commit()
print('Done.')

print("Found", cur.execute('SELECT COUNT(identity) FROM authors;').fetchall(), "authors")

# get books

cur.close()
