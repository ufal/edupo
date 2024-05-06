import sqlite3

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

db = sqlite3.connect('new.db')
cur = db.cursor()

cur.execute('ALTER TABLE authors ADD COLUMN zena BOOLEAN;')

for z in zeny:
    #print(cur.execute("SELECT * FROM authors WHERE identity = ?", (z,)).fetchall())
    cur.execute("UPDATE authors SET zena = 1 WHERE identity = ?", (z,))

db.commit()
db.close()