#!/usr/bin/env python3
#coding: utf-8

import sys
import math
import json
import glob
sys.path.append("../kveta")
from kveta import okvetuj
from collections import defaultdict

def get_rhyme_scheme(numbers):
    num2id = dict()
    n = 0
    scheme = "-"
    for num in numbers:
        if num == None:
            scheme += '0-'
        elif num in num2id:
            scheme += str(num2id[num]) + '-'
        else:
            n += 1
            num2id[num] = n
            scheme += str(n) + '-'
    return scheme

def get_measures(input_txt):

    data, k = okvetuj(input_txt)

    poem = data[0]["body"]
    
    unknown_counter = 0
    words_counter = 0
    rhyme_count = 0
    metre_probs_sum = defaultdict(float)
    num_syllables_count = defaultdict(int)
    rhyme_schemes = defaultdict(int)
    
    current_stanza_num = -1
    current_stanza = []
    
    for i in range(len(poem)):
        syllcount = 0
        for word in poem[i]['words']:
            if 'is_unknown' in word:
                unknown_counter += 1
            words_counter += 1
            if 'syllables' in word:
                syllcount += len(word['syllables'])
        num_syllables_count[syllcount] += 1
        if 'rhyme' in poem[i] and poem[i]["rhyme"] != None:
            rhyme_count += 1
        if 'metre_probs' in poem[i]:
            for m in ['T', 'J', 'D', 'A']:
                if m in poem[i]['metre_probs']:
                    metre_probs_sum[m] += poem[i]['metre_probs'][m]
        if poem[i]['stanza'] != current_stanza_num:
            if current_stanza:
                rhyme_schemes[get_rhyme_scheme(current_stanza)] += 1
                current_stanza = []
            current_stanza_num = poem[i]['stanza']
        current_stanza.append(poem[i]['rhyme'])

        syllable_count_entropy = 0 # unigram entropy on syllable counts
        for c in num_syllables_count:
            syllable_count_entropy -= num_syllables_count[c] / len(poem) * math.log2(num_syllables_count[c] / len(poem))
    
    if current_stanza:
        rhyme_schemes[get_rhyme_scheme(current_stanza)] += 1

    return {'unknown_words': unknown_counter/words_counter,
            'rhyming': rhyme_count / len(poem),
            'metre_consistency': max(metre_probs_sum.values()) / len(poem),
            'syllable_count_entropy': syllable_count_entropy,
            'rhyming_consistency': max(rhyme_schemes.values()) / (current_stanza_num + 1)
            }

if __name__=="__main__":

    print('name', 'unknown_words', 'rhyming', 'metre_consistency', 'syllable_count_entropy', 'rhyming_consistency', sep="\t")
    for path in sys.argv[1:]:
        for filename in glob.glob(path):
            with open(filename, 'r') as file:
                input_text = ""
                if filename.endswith('.json'):
                    # convert json to raw txt
                    data = json.load(file)
                    for s in range(len(data[0]["body"])):
                        for l in range(len(data[0]["body"][s])):
                            input_text += data[0]["body"][s][l]["text"] + "\n"
                        input_text += "\n"
                else:
                    input_text = file.read()
            try:
                results = get_measures(input_text)
            except:
                print('ERROR while processing file:', filename, file=sys.stderr)
                raise
            print(filename, results['unknown_words'], results['rhyming'], results['metre_consistency'], results['syllable_count_entropy'], results['rhyming_consistency'], sep="\t")
