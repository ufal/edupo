import csv
import sys
import re

csv_file = sys.argv[1]

with open(csv_file, 'r') as f:
    dataset = [w for w in csv.DictReader(f, delimiter=';')]

key = 'Ortho'
if key not in dataset[0]:
    key = 'Name'

dataset = [(x[key].lower(), x['Syllab']) for x in dataset]

diphthongs_dict = {'ou': 'ö', 'au': 'ä',  'eu': 'ë'}
d_out = list(diphthongs_dict.values()) + ['o.u', 'a.u', 'e.u', 'o-u', 'a-u', 'e-u']

dataset_new = []

for t, f in dataset:
    d_count_in, d_count_out = 0, 0
    for d in diphthongs_dict.keys():
        d_count_in += t.count(d)
    for d in d_out:
        d_count_out += f.count(d)
    
    if d_count_in > 0 and d_count_in == d_count_out and '-' not in t and ' ' not in t:
        dataset_new.append((t, f))

for t, f in dataset_new:
    matches_in = re.findall(r'|'.join(diphthongs_dict.keys()), t)
    # find positions of the matches in t

    positions = [m.start() for m in re.finditer(r'|'.join(diphthongs_dict.keys()), t)]

    matches_out = re.findall(r'|'.join([x.replace('.', '\\.') for x in d_out]), f)
    assert len(matches_in) == len(matches_out), (t, f, matches_in, matches_out)
    slovo = list(t)
    posun = 0
    for i, o, p in zip(matches_in, matches_out, positions):
        if o in diphthongs_dict.values():
            continue
        else:
            slovo.insert(p + posun + 1, '-')
            posun += 1 
    print(''.join(slovo))
