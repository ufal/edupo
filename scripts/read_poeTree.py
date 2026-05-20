import json
import zipfile
import sys

zfile = 'poeTree/cs.zip'

if sys.argv[1] == 'authors':
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
            a, w = poem_f['author']['name'], poem_f['author']['wiki']
            if a not in authors:
                authors[a] = w
            else:
                assert authors[a] == w
    for a in authors:
        print(a, authors[a], sep='\t')

elif sys.argv[1] == 'duplicates':
    with zipfile.ZipFile(zfile, 'r') as z:
        files = [x for x in z.namelist() if not z.getinfo(x).is_dir()]
        for fname in files:
            with z.open(fname) as f:
                try:
                    poem_f = json.loads(f.read())
                except:
                    print(fname)
                    sys.exit(1)
            if poem_f['duplicate'] != False:
                print(poem_f['id'], poem_f['duplicate'], poem_f['title'], poem_f['author']['name'], sep='\t')