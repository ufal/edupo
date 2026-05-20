import sqlite3
import sys

db_filename = "new.db"

if sys.argv[1] == 'authors':
    with open('auth_wiki') as f:
        a = f.readlines()            
        a = [x[:-1].split('\t') for x in a]

    with sqlite3.connect(db_filename) as db:
        db.execute("BEGIN TRANSACTION;")
        db.execute("ALTER TABLE authors ADD COLUMN wiki STRING;")

        for au, wik in a:
            id = db.execute("SELECT DISTINCT author FROM poems WHERE author_name = ?;", (au,)).fetchall()[0][0]
            print(id)
            db.execute("UPDATE authors SET wiki = ? WHERE identity = ?;", (wik, id))

elif sys.argv[1] == 'duplicates':
    with open('dupl_plechac') as f:
        a = f.readlines()            
        a = [x.split('\t')[:2] for x in a]

    with sqlite3.connect(db_filename) as db:
        db.execute("BEGIN TRANSACTION;")
        db.execute("ALTER TABLE poems ADD COLUMN duplicate_plechac INT REFERENCES poems(id);")

        for poem, dupl in a:
            if poem == dupl:
                print("DUPLICATE OF ITSELF", poem)
                continue
            poem = poem.split('_')
            dupl = dupl.split('_')
            try:
                id = db.execute("SELECT id FROM poems WHERE book_id = ? AND poem_id_corp = ?;", poem).fetchall()
                dupl_id = db.execute("SELECT id FROM poems WHERE book_id = ? AND poem_id_corp = ?;", dupl).fetchall()
                assert len(id) == 1 and len(dupl_id) == 1
                id, dupl_id = id[0][0], dupl_id[0][0]
            except Exception as e:
                print(poem, dupl)
                raise e
            db.execute("UPDATE poems SET duplicate_plechac = ? WHERE id = ?;", (dupl_id, id))

elif sys.argv[1] == 'normalize':
    with sqlite3.connect(db_filename) as db:
        db.execute("BEGIN TRANSACTION;")
        db.execute("ALTER TABLE poems ADD COLUMN duplicate_plechac_norm INT REFERENCES poems(id);")
        canonical = [x[0] for x in db.execute("SELECT DISTINCT duplicate_plechac FROM poems WHERE duplicate_plechac IS NOT NULL;").fetchall()]
        for c in canonical:
            poems = [x[0] for x in db.execute("SELECT id FROM poems WHERE duplicate_plechac = ?;", (c,)).fetchall()] + [c]
            print(c, poems)
            lst = db.execute('SELECT year, poems.id FROM poems JOIN books ON poems.book_id=books.id WHERE poems.id IN ({})'.format(','.join(str(x) for x in poems))).fetchall()
            lst = [(y, i) if (y != 'neuveden') else (0, i) for y, i in lst]
            print(lst)
            lst.sort()
            kanonic = lst[-1][1]
            print(kanonic)
            print("=" * 80)
            db.execute('UPDATE poems SET duplicate_plechac_norm={} WHERE id IN ({})'.format(kanonic, ','.join([str(id) for _, id in lst[:-1]])))