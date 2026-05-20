import sqlite3
import json
import time

cas = time.time()
print('Reading original database.', end=' ')
with sqlite3.connect('../data/KCV_komplet/cs.db') as db:
    jsons = db.execute("select p_object from main;").fetchall()
print('Done in {:.2f} s.'.format(time.time() - cas))


cas = time.time()
print('Converting JSONs.', end=' ')
jsons = [json.loads(j[0]) for j in jsons]
print('Done in {:.2f} s.'.format(time.time() - cas))

print('Creating authors table.', end=' ')
authors = [j['p_author'] for j in jsons] + [j['b_author'] for j in jsons]
a_dict = {}
for a in authors:
    if a['identity'] in a_dict:
        assert a_dict[a['identity']]['born'] == a['born']
        assert a_dict[a['identity']]['died'] == a['died']
    else:
        a_dict[a['identity']] = a
print('Done.')

def norm_year(year):
    if year == 'neuveden':
        return 0
    if year[0] == '[' and year[-1] == ']':
        year = year[1:-1]
    return int(year)

print('Creating books table.', end=' ')
b_dict = {}
for b in jsons:
    id = int(b['book_id'])
    if id in b_dict:
        for k in b['biblio']:
            if k == 'p_title':
                continue
            if k == 'year':
                assert b_dict[id][k] == norm_year(b['biblio'][k]), (id, k, b_dict[id][k], norm_year(b['biblio'][k]))
                continue
            assert b_dict[id][k] == b['biblio'][k], (id, k, b_dict[id][k], b['biblio'][k])
        assert b_dict[id]['author'] == b['b_author']['identity']
    b_dict[id] = dict()
    b_dict[id]['id'] = id
    for k in b['biblio']:
        if k == 'p_title':
                continue
        if k == 'year':
            b_dict[id][k] = norm_year(b['biblio'][k])
            continue
        b_dict[id][k] = b['biblio'][k]
    b_dict[id]['author'] = b['b_author']['identity']
    b_dict[id]['author_name'] = b['b_author']['name']
print('Done.')

def old_to_new(b):
    # flatten the body stanza structure
    for i, stanza in enumerate(b['body']):
        for line in stanza:
            line['stanza'] = i
    b['body'] = sum(b['body'], [])
    # fix the meters format
    for line in b['body']:
        lst = []
        for x in line['metre']:
            assert len(x) == 1
            lst.append(list(x.items())[0])
        line['metre'] = {a:b for a, b in lst}

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
    old_to_new(b)
    p_dict[id]['body'] = b['body']
print('Done.')

print('Creating new database.', end=' ')
with sqlite3.connect("new.db") as db:
    db.execute("CREATE TABLE authors (identity STRING PRIMARY KEY, born YEAR, died YEAR);")
    for a in a_dict.values():
        db.execute("INSERT INTO authors VALUES (?, ?, ?);", (a['identity'], a['born'], a['died']))
    db.execute("CREATE TABLE books (id INT PRIMARY KEY, title STRING, subtitle STRING, author STRING REFERENCES authors(identity)," + \
                " author_name STRING, motto STRING, motto_aut STRING," + \
                " publisher STRING, edition STRING, place STRING, dedication STRING, pages STRING, year YEAR, signature STRING);")
    for b in b_dict.values():
        db.execute("INSERT INTO books VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
                    (b['id'], b['b_title'], b['b_subtitle'], b['author'], b['author_name'], b['motto'], b['motto_aut'], b['publisher'], b['edition'],
                    b['place'], b['dedication'], b['pages'], b['year'], b['signature']))
    db.execute("CREATE TABLE poems (id INT PRIMARY KEY, book_id INT REFERENCES books(id), author STRING REFERENCES authors(identity)," + \
                " author_name STRING, title STRING, poem_id_corp STRING," + \
                " schools JSON, schemes JSON, body JSON);")
    for p in p_dict.values():
        db.execute("INSERT INTO poems VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);",
                    (p['id'], p['book_id'], p['author'], p['author_name'], p['title'], p['poem_id_corp'],
                    json.dumps(p['schools'], ensure_ascii=False), json.dumps(p['schemes'], ensure_ascii=False), json.dumps(p['body'], ensure_ascii=False),
                    ))
    db.commit()
    print('Done.')

    print('Fixing bugs in the data.', end=' ')

    # Nové národní písně | Horký, Karel
    db.execute('UPDATE books SET year=1915 WHERE id=1687;')
    db.commit()

    print('Done.')

    print('Adding author wiki links.', end=' ')
    with open('auth_wiki') as f:
        a = f.readlines()            
        a = [x[:-1].split('\t') for x in a]

    db.execute("BEGIN TRANSACTION;")
    db.execute("ALTER TABLE authors ADD COLUMN wiki STRING;")

    for au, wik in a:
        if wik == '':
            continue
        id = db.execute("SELECT DISTINCT author FROM poems WHERE author_name = ?;", (au,)).fetchall()[0][0]
        db.execute("UPDATE authors SET wiki = ? WHERE identity = ?;", (wik, id))
    db.commit()
    print('Done.')

    print('Adding author gender.', end=' ')
    zeny= [
        'Benešová, Božena',
        'Geisslová, Irma',
        'Jesenská, Růžena',
        'Krásnohorská, Eliška',
        'Maternová, Pavla',
        'Mühlsteinová, Berta',
        'Němcová, Božena',
        'Pilbauerová, Herma',
        'Růžičková, Anna Vlastimila',
        'Simerská, Anna',
        'Čacká, Marie',
        'Šimková-Uzlová, Fanda',
        # KCV_komplet
        'Calma, Marie',
        'Dubrovská, Tereza',
        'Bubelová, Lila',
        'Schwarzová, Růžena',
        'Šárecká, Maryša',
        'Vášová, Věra',
        'Baarová, Marie',
        'Menčlová, Antonie',
        'Sázavská, Anna',
        'Jeřábková, Růžena B.',
        'Hrdličková, Bohdana',
        'Studničková, Božena',
        'Knauerová, Fanča',
        'Trojanová, Olga',
        'Hoffmannová, Antonie',
        'Těšínská, Marie',
        'Záhořová, Milada',
        'Lešková, Rebeka',
        'Kavánová, Marie',
        'Rozsypalová, Augusta',
        'Podlipská, Sofie',
        'Karbanová, Bohumila',
        'Slavinská, Marie',
        'Dvořáková-Mráčková, Albína',
        'Hradecká, Jasa',
    ]

    db.execute("BEGIN TRANSACTION;")
    db.execute('ALTER TABLE authors ADD COLUMN zena BOOLEAN;')
    for z in zeny:
        db.execute("UPDATE authors SET zena = 1 WHERE identity = ?", (z,))
    db.commit()
    print('Done.')

    print('Adding info about duplicates.', end=' ')
    duplicates = []
    for filename in [
            'duplicates/phase1',
            'duplicates/phase2',
            'duplicates/phase3',
        ]:
        with open(filename) as f:
            d = f.readlines()
            duplicates += [x.split() for x in d]
    db.execute("BEGIN TRANSACTION;")
    db.execute('ALTER TABLE poems ADD COLUMN duplicate INT REFERENCES poems(id);')

    for d in duplicates:
        canonical = d[0]
        for p in d[1:]:
            db.execute("UPDATE poems SET duplicate = ? WHERE id = ?", (canonical, p))
    db.commit()
    print('Done.')