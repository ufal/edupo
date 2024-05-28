with open('auth_wiki') as f:
    a = f.readlines()            
    a = [x[:-1].split('\t') for x in a]

import sqlite3

db_filename = "new.db"

with sqlite3.connect(db_filename) as db:
    db.execute("BEGIN TRANSACTION;")
    db.execute("ALTER TABLE authors ADD COLUMN wiki STRING;")

    for au, wik in a:
        id = db.execute("SELECT DISTINCT author FROM poems WHERE author_name = ?;", (au,)).fetchall()[0][0]
        print(id)
        db.execute("UPDATE authors SET wiki = ? WHERE identity = ?;", (wik, id))    
