#!/usr/bin/python3

import sys
import json
import phonetix
import syllables
import rhyme
import kveta

filename = sys.argv[1]
output_filename = sys.argv[2]

print("Processing", filename, file=sys.stderr)

f = open(filename, "r")
data = json.load(f)
stanza = 0
new_body = []
for i in range(len(data[0]["body"])):
    for j in range(len(data[0]["body"][i])):
        data[0]["body"][i][j]["stanza"] = stanza
        new_body.append(data[0]["body"][i][j])
    stanza += 1

data[0]["body"] = kveta.okvetuj_ccv(new_body)
#ptx = phonetix.Phonetix()
#new_body = ptx.phoebe2cft(new_body)
#syl = syllables.Syllables()
#new_body = syl.split_words_to_syllables(new_body)
#rt = rhyme.RhymeDetection(window=6, probability_sampa_min=0.95, probability_ngram_min=0.95)
#new_body = rt.mark_reduplicants(new_body)
#data[0]["body"] = new_body

# evaluate counts of syllables
for i, l in enumerate(new_body):
    syll_cnt_our = 0
    for j, w in enumerate(l['words']):
        if w["syllables"]:
            syll_cnt_our += len(w["syllables"])
    syll_cnt_ccv = len(l["sections"])
    if syll_cnt_our != syll_cnt_ccv:
        print("Syllable counts do not match:", l['text'], file=sys.stderr)

f = open(output_filename, "w")
json.dump(data, f, ensure_ascii=False, indent=4)
f.close()
