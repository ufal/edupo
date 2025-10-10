#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append("../kveta")
from kveta import okvetuj
from get_measures import get_measures

print('filename', 'unknown_words', 'rhyming', 'metre_consistency', 'syllable_count_entropy', 'rhyming_consistency', 'chatgpt_meaning', 'chatgpt_syntax', 'chatgpt_rhyming', 'chatgpt_language', 'chatgpt_metrum', sep="\t")

for i in range(1, 1000):
    num = str(i)
    #if len(num) < 2:
    #    num = '0'+num
    filename = "poems/chatgpt-4o/poem_" + num + ".txt"
    if not os.path.isfile(filename):
        continue
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
            results = get_measures(content)
    except:
        print('ERROR while processing', filename, file=sys.stderr)
        
    if results:
        print(filename, results['unknown_words'], results['rhyming'], results['metre_consistency'], results['syllable_count_entropy'], results['rhyming_consistency'], results['chatgpt_meaning'], results['chatgpt_syntax'], results['chatgpt_rhyming'], results['chatgpt_language'], results['chatgpt_metrum'], sep="\t", flush=True)
    results = {}

