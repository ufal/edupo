#!/usr/bin/env python3
#coding: utf-8

import sys
sys.path.append("../kveta")
from kveta import okvetuj

def get_measures(filename):

    text = ""
    hints = []

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            items = line.split('#')
            if len(items) >= 5:
                verse = items[4].strip()
                if verse:
                    hints.append([items[1].strip(), items[2].strip(), items[3].strip()])
                    text += verse + "\n"
            elif line == "":
                text += "\n"
    f.close()

    data, k = okvetuj(text)

    if len(data[0]["body"][0]) != len(hints):
        print("ERROR: The output length is different from the output length:", len(data[0]["body"][0]), len(hints))
        return {}

    unknown_counter = 0
    words_counter = 0
    syllable_count_match = 0
    meter_match = 0

    for i in range(len(hints)):
        #if 'metre' in data[0]["body"][0][i] and hints[i][0] in data[0]["body"][0][i]['metre'][0]:
        #    meter_match += 1
        #print(data[0]["body"][0][i]['text'], hints[i][0], data[0]["body"][0][i]['metre'][0])
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
            #'meter_acc': meter_match / len(hints),
            'syllable_cnt_acc': syllable_count_match / len(hints) }


if __name__=="__main__":

    results = get_measures(sys.argv[1])

    print(results)
