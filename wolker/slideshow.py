#!/usr/bin/env python3
#coding: utf-8

import common
import os
import os.path
import random

OUTPUTDIR = 'genouts'

def getctime(item):
    item_path = os.path.join(OUTPUTDIR, item)
    return os.path.getctime(item_path)

def choose_candidate():
    candidates = os.listdir(OUTPUTDIR)

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
    
    return f'{OUTPUTDIR}/{candidate}'

def main():
    files = [
        'header_refresh.html',
        choose_candidate(),
        'footer.html',
    ]
    return [common.return_file(f) for f in files]

if __name__=="__main__":
    print(main(), sep='\n')

