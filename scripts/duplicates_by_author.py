import sqlite3
import json
import time
import sys

from Levenshtein import distance, ratio

db_filename = "new.db"

db = sqlite3.connect(db_filename)
cur = db.cursor()
counts = cur.execute("SELECT COUNT(id), author FROM poems GROUP BY author;").fetchall()

counts = [(c, a) for c, a in counts if c > 1]

# print(sum([(c * (c - 1)) // 2 for c, _ in  counts]))
total = 59944868

def poem_text(poem):
    sloky = []
    for sloka in poem:
        lines = []
        for line in sloka:
            lines.append(line['text']) 
        sloky.append('\n'.join(lines))
    return '\n\n'.join(sloky)

i = 1
t_start = time.time()
for c, a in counts:
    print(c, a, file=sys.stderr)
    poems = cur.execute("SELECT id, body FROM poems WHERE author = ?;", (a,)).fetchall()
    poems = [(i, poem_text(json.loads(poem))) for i, poem in poems]
    for a in poems:
        for b in poems:
            if a[0] <= b[0]:
                continue
            p1, p2 = a[1], b[1]
            if len(p1) < len(p2):
                p1, p2 = p2, p1
            r = ratio(p1, p2)
            if r > 0.6:
                print(a[0], b[0], distance(p1, p2), r)
            i += 1
            if i % 100000 == 0:
                print(i, i/total, time.time() - t_start, "ETA:", (time.time() - t_start) * total / (i* 60), "mins",
                      file=sys.stderr)
