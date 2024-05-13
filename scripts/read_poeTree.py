import json
import zipfile
import os
import sys

zfile = 'poeTree/cs.zip'
i = 1

authors = dict()
with zipfile.ZipFile(zfile, 'r') as z:
    files = [x for x in z.namelist() if not z.getinfo(x).is_dir()]
    for fname in files:
        with z.open(fname) as f:
            try:
                poem_f = json.loads(f.read())
            except:
                print(fname)
                sys.exit(1)
        print(poem_f['author'])
        sys.exit(0)
        a, w = poem_f['author']['name'], poem_f['author']['wiki']
        if a not in authors:
            authors[a] = w
        else:
            assert authors[a] == w
        i += 1
        
        if i % 1000 == 0:
            print(i, file=sys.stderr)

for a in authors:
    print(a, authors[a], sep='\t')