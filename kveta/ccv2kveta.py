#!/usr/bin/python3

import sys
import json
import phonetix
import syllables

filename = sys.argv[1]
output_filename = sys.argv[2]

f = open(filename, "r")
data = json.load(f)
stanza = 0
new_body = []
for i in range(len(data[0]["body"])):
    for j in range(len(data[0]["body"][i])):
        data[0]["body"][i][j]["stanza"] = stanza
        new_body.append(data[0]["body"][i][j])
    stanza += 1

ptx = phonetix.Phonetix()
new_body = ptx.phoebe2cft(new_body)
syl = syllables.Syllables()
new_body = syl.split_words_to_syllables(new_body)

data[0]["body"] = new_body

f = open(output_filename, "w")
json.dump(data, f, ensure_ascii=False, indent=4)
f.close()
