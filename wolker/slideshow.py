#!/usr/bin/env python3
#coding: utf-8

import common
import os
import os.path
import random

common.header_refresh()

print('<a href="index.py">Zpátky na začátek</a>')
print('<br>')

DIR = 'genouts'

def getctime(item):
    item_path = os.path.join(DIR, item)
    return os.path.getctime(item_path)

candidates = os.listdir(DIR)

# randomly choose whether to use weights or not
if random.randint(0, 1) == 0:
    candidate = random.choice(candidates)
else:
    # assert == 1
    candidates.sort(key=getctime, reverse=True)
    weights = []
    weight = 1
    decay = 0.7
    for candidate in candidates:
        weights.append(weight)
        weight *= decay
    candidate = random.choices(candidates, weights=weights)[0]

common.write_out_file(f'genouts/{candidate}')
    
common.footer()
