#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append("../kveta")
from kveta import okvetuj
from get_measures import get_measures

input_dir = sys.argv[1]
output_file = sys.argv[2]
measures = ('unknown_words', 'rhyming', 'metre_accuracy', 'chatgpt_meaning')
avg=dict()
total = 0

#print('filename', 'unknown_words', 'rhyming', 'metre_consistency', 'syllable_count_entropy', 'rhyming_consistency', 'chatgpt_meaning', 'chatgpt_syntax', 'chatgpt_rhyming', 'chatgpt_language', 'chatgpt_metrum', sep="\t")

with open(output_file, "w") as f:
    f.write('filename')
    for m in measures:
        f.write("\t"+m)
        avg[m] = 0
    f.write("\n")
    for i in range(1, 1000):
        num = str(i)
        filename = input_dir+"/poem_" + num + ".txt"
        if not os.path.isfile(filename):
            continue
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()
                results = get_measures(content)
        except:
            print('ERROR while processing', filename, file=sys.stderr)
        
        if results:
            print (f"poem_{num} processed", file=sys.stderr)
            total += 1
            f.write(filename)
            for m in measures:
                f.write("\t"+str(results[m]))
                avg[m] += float(results[m])
            f.write("\n")
        results = {}

for m in measures:
    print("Average", m, ":", str(avg[m]/total))
f.close()

