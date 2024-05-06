import sqlite3
import json
import time
import sys

from akin import MinHash, LSH
from Levenshtein import distance, ratio

db_filename = "new.db"

db = sqlite3.connect(db_filename)
cur = db.cursor()
jsons = cur.execute("SELECT id, body FROM poems;").fetchall()
db.close()

poems = []
ids = []
for i, poem in jsons:
    poem = json.loads(poem)
    sloky = []
    for sloka in poem:
        lines = []
        for line in sloka:
            lines.append(line['text']) 
        sloky.append('\n'.join(lines))
    poems.append('\n\n'.join(sloky))
    ids.append(i)

k = 5000
max_l = len(poems)
lsh = LSH(no_of_bands=25)

for i in range((max_l//k)+1):
    start_from = i*k
    up_to = min((i+1)*k, max_l)
    print('Processing', start_from, 'to', up_to, 'out of', max_l, 'poems', file=sys.stderr)
    start = time.time()
    # Generate MinHash signatures
    signatures = MinHash(poems[i*k: min((i+1)*k, max_l)], n_gram=5, permutations=100, hash_bits=64, seed=7)
    end = time.time()
    print('Generating MinHash signatures took', end - start, 'seconds,', (end - start)/k, 'per poem,',
          ((end - start)* (max_l- up_to) / k / 60), 'minutes estimated for all poems', file=sys.stderr)

    # Update LSH model.
    start = time.time()
    lsh.update(signatures, ids[start_from:up_to])
    end = time.time()
    print('Creating LSH model took', end - start, 'seconds', file=sys.stderr)

start = time.time()
duplicates = dict()
for i in ids:
    near_duplicates = lsh.query(i, min_jaccard=0.001, sensitivity=1)
    if near_duplicates:
        for j in near_duplicates:
            if j not in duplicates:
                duplicates[j] = set(near_duplicates + [i]) - {j}
            else:
                duplicates[j].update(set(near_duplicates + [i]) - {j})
end = time.time()
print('Querying LSH model took', end - start, 'seconds,', file=sys.stderr)
print(len(duplicates), file=sys.stderr)

for k, v in duplicates.items():
    for i in v:
        print(k, i, distance(poems[k], poems[i]), ratio(poems[k], poems[i]))
    