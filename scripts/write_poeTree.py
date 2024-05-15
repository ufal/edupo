with open('auth_wiki') as f:
    a = f.readlines()            
    a = [x[:-1].split('\t') for x in a]

import sqlite3

db_filename = "new.db"

db = sqlite3.connect(db_filename)

cur = db.cursor()

#cur.execute("ALTER TABLE authors ADD COLUMN wiki STRING;")

for au, wik in a:
    id = cur.execute("SELECT DISTINCT author FROM poems WHERE author_name = ?;", (au,)).fetchall()[0][0]
    print(id)
    cur.execute("UPDATE authors SET wiki = ? WHERE identity = ?;", (wik, id))

db.commit()

db.close()
    
