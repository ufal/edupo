import re
import sys

with open(sys.argv[1], 'r') as f:
    dataset = [w.split(',') for w in  f.read().splitlines()]

diphthongs_dict = {'ou': '0', 'au': '1',  'eu': '2'}
d_out = list(diphthongs_dict.keys()) + list(diphthongs_dict.values())

dataset_new = []

for t, f in dataset:
    d_count_in, d_count_out = 0, 0
    for d in diphthongs_dict.keys():
        d_count_in += t.count(d)
    for d in d_out:
        d_count_out += f.count(d)
    
    if d_count_in == d_count_out:
        dataset_new.append((t, f))



for t, f in dataset_new:
    matches_in = re.findall(r'|'.join(diphthongs_dict.keys()), t)
    # find positions of the matches in t

    positions = [m.start() for m in re.finditer(r'|'.join(diphthongs_dict.keys()), t)]

    matches_out = re.findall(r'|'.join(d_out), f)
    assert len(matches_in) == len(matches_out)
    slovo = list(t)
    posun = 0
    for i, o, p in zip(matches_in, matches_out, positions):
        if o in diphthongs_dict.values() or o != i:
            continue
        else:
            slovo.insert(p + posun + 1, '-')
            posun += 1 
    print(''.join(slovo))
            