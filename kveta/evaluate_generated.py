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
        items = line.split('#')
        if len(items) >= 4 and len(items[0].strip()) > 0 and items[1].strip().isdigit():
            verse = items[3].strip()
            if verse:
                hints.append([items[0].strip(), items[1].strip(), items[2].strip()])
                text += verse + "\n"
        elif line == "":
            text += "\n"

    data, k = okvetuj(text)

    if len(data[0]["body"][0]) != len(hints):
        print("ERROR: The output length is different from the output length:", len(data[0]["body"][0]), len(hints))
        return {}

    unknown_counter = 0
    words_counter = 0
    syllable_count_match = 0
    metre_average_prob = 0

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

    return {'unknown_words': unknown_counter/words_counter,
            'metre_average_prob': metre_average_prob / len(hints),
            'syllable_cnt_acc': syllable_count_match / len(hints) }


if __name__=="__main__":

    with open(sys.argv[1], 'r') as f:
        input_text = f.read()

    results = get_measures(input_text)

    print(results)
