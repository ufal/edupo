#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append("../kveta")
from kveta import okvetuj
from get_measures import get_measures

print('filename', 'unknown_words', 'rhyming', 'metre_consistency', 'syllable_count_entropy', 'rhyming_consistency', 'chatgpt_meaning', 'chatgpt_syntax', 'chatgpt_rhyming', 'chatgpt_language', 'chatgpt_metrum', sep="\t")

for i in range(51, 101):
    filename = "poems/poem_" + str(i) + ".txt"
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
    try:
        results = get_measures(content)
    except:
        print('ERROR while processing', filename, file=sys.stderr)
        raise
    print(filename, results['unknown_words'], results['rhyming'], results['metre_consistency'], results['syllable_count_entropy'], results['rhyming_consistency'], results['chatgpt_meaning'], results['chatgpt_syntax'], results['chatgpt_rhyming'], results['chatgpt_language'], results['chatgpt_metrum'], sep="\t", flush=True)

