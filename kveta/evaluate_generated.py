#!/usr/bin/env python3
#coding: utf-8

import sys
sys.path.append("../kveta")
from kveta import okvetuj

def get_measures(input_txt):

    text = ""
    hints = []

    for line in input_txt.split("\n"):
        line = line.strip()
        if line.startswith('#'):
            line = line[1:].strip()
        items = [v.strip() for v in line.split('#')]
        if len(items) >= 4 and len(items[0]) > 0 and items[0] != 'N' and items[1].isdigit() and items[2] != 'NON' and len(items[3]) > 0:
            hints.append([items[0], items[1], items[2]])
            text += items[3] + "\n"
        elif line == "":
            text += "\n"

    data, k = okvetuj(text)

    if len(data[0]["body"][0]) != len(hints):
        print("ERROR: The output length is different from the hints length:", len(data[0]["body"][0]), len(hints))
        return {}

    unknown_counter = 0
    words_counter = 0
    syllable_count_match = 0
    metre_average_prob = 0
    rhyme_count = 0

    for i in range(len(hints)):
        if 'metre_probs' in data[0]["body"][0][i]:
            if hints[i][0] in data[0]["body"][0][i]['metre_probs']:
                metre_average_prob += data[0]["body"][0][i]['metre_probs'][hints[i][0]]
            elif hints[i][0] == 'N':
                # pro neurcite metrum je vzdy vsechno spravne
                metre_average_prob += 1

        syllcount = 0
        for word in data[0]["body"][0][i]['words']:
            if 'is_unknown' in word:
                unknown_counter += 1
            words_counter += 1
            if 'syllables' in word:
                syllcount += len(word['syllables'])
        if syllcount == int(hints[i][1]):
            syllable_count_match += 1
        if 'rhyme' in data[0]["body"][0][i] and data[0]["body"][0][i]["rhyme"] != None:
            rhyme_count += 1


    return {'unknown_words': unknown_counter/words_counter,
            'metre_average_prob': metre_average_prob / len(hints),
            'syllable_cnt_acc': syllable_count_match / len(hints),
            'rhyming': rhyme_count / len(hints),
            'correct_lines': len([t for t in text if len(t.strip()) > 0]),
            }

if __name__=="__main__":

    with open(sys.argv[1], 'r') as f:
        input_text = f.read()
    
    try:
        results = get_measures(input_text)
    except:
        print('ERROR while processing file:', sys.argv[1], file=sys.stderr)
        raise

    print(sys.argv[1], results)
