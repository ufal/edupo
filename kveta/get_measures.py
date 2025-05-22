#!/usr/bin/env python3
#coding: utf-8

import sys
import math
import json
import glob
sys.path.append("../kveta")
from kveta import okvetuj
from collections import defaultdict
from openai import OpenAI
sys.path.append("../backend")
from openai_helper import generate_with_openai_simple

def get_rhyme_scheme(numbers):
    num2id = dict()
    n = 0
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVYZ"
    scheme = []
    
    # nejprve spočítam kolikrát se ve stanze objevuje daný rým
    numcnt = defaultdict(int)
    for num in numbers:
        numcnt[num] += 1

    # mapování čísel na písmenka
    for num in numbers:
        if num == None or numcnt[num] == 1:
            scheme.append('X')
        elif num in num2id:
            scheme.append(num2id[num])
        else:
            num2id[num] = alphabet[n]
            scheme.append(num2id[num])
            n += 1

    return "".join(scheme)

def get_measures_from_analyzed_poem(poem, parameters={}):

    if not 'rhyme_scheme' in parameters:
        parameters['rhyme_scheme'] = None
    if not 'metre' in parameters:
        parameters['metre'] = None

    unknown_counter = 0
    words_counter = 0
    rhyme_count = 0
    metre_probs_sum = defaultdict(float)
    #metre_probs_rb = defaultdict(float)
    num_syllables_count = defaultdict(int)
    rhyme_schemes = defaultdict(int)
    #syllables_total = 0

    rhyme_scheme_correct = 0
    rhyme_scheme_total = 0
    
    current_stanza_num = -1
    current_stanza = []
   
    raw_text = ""
    for i in range(len(poem)):
        syllcount = 0
        raw_text += poem[i]['text'] + "\n"
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
        #if 'sections' in poem[i]:
        #    for j, stress in enumerate(poem[i]['sections']):
        #        if j % 2 == 0 or stress == 0:
        #            metre_probs_rb['T'] += 1
        #        if j % 2 == 1 or stress == 0:
        #            metre_probs_rb['J'] += 1
        #        if j % 3 == 0 or stress == 0:
        #            metre_probs_rb['D'] += 1
        #        if j % 3 == 1 or stress == 0:
        #            metre_probs_rb['A'] += 1
        #        syllables_total += 1

        if poem[i]['stanza'] != current_stanza_num:
            if current_stanza:
                rs = get_rhyme_scheme(current_stanza)
                if parameters['rhyme_scheme'] == rs:
                    rhyme_scheme_correct += 1
                rhyme_scheme_total += 1
                rhyme_schemes[rs] += 1
                current_stanza = []
            current_stanza_num = poem[i]['stanza']
        current_stanza.append(poem[i]['rhyme'])

        syllable_count_entropy = 0 # unigram entropy on syllable counts
        for c in num_syllables_count:
            syllable_count_entropy -= num_syllables_count[c] / len(poem) * math.log2(num_syllables_count[c] / len(poem))
    
    if current_stanza:
        rs = get_rhyme_scheme(current_stanza)
        if parameters['rhyme_scheme'] == rs:
            rhyme_scheme_correct += 1
        rhyme_scheme_total += 1
        rhyme_schemes[rs] += 1

    # ChatGPT init
    #KEY_PATH = '/net/projects/EduPo/data/apikey.txt'
    #with open(KEY_PATH) as infile:
    #    apikey = infile.read().rstrip()
    #try:
    #    client = OpenAI(api_key=apikey)
    #except:
    #    logging.exception("EXCEPTION Neúspěšná inicializace OpenAI.")

    # ChatGPT metrics
    #meaning_response = client.responses.create(
    #    model="gpt-4.1",
    #    input="Na škále 1 až 10 ohodnoť smysluplnost následující básně. Napiš pouze to číslo.\n\n" + raw_text
    #)
    
    response = generate_with_openai_simple("Na škále 1 až 10 ohodnoť smysluplnost následující básně. Napiš pouze to číslo.\n\n" + raw_text)
    meaning_num = int(response.strip())
    if meaning_num > 0 and meaning_num <= 10:
        meaning_num /= 10
    else:
        meaning_num = 0

    return {'unknown_words': unknown_counter/words_counter,
            'rhyming': rhyme_count / len(poem),
            'rhyme_scheme_accuracy': rhyme_scheme_correct / rhyme_scheme_total,
            'metre_consistency': max(metre_probs_sum.values()) / len(poem),
            'metre_accuracy': metre_probs_sum[parameters['metre']] / len(poem),
            #'metre_consistency_rb': max(metre_probs_rb.values()) / syllables_total,
            'syllable_count_entropy': syllable_count_entropy,
            'rhyming_consistency': max(rhyme_schemes.values()) / (current_stanza_num + 1),
            'meaningfulness': meaning_num
           }

def get_measures(input_txt, parameters={}):

    data, k = okvetuj(input_txt)

    return get_measures_from_analyzed_poem(data[0]["body"], parameters)

if __name__=="__main__":
    parameters = {}
    if len(sys.argv) >= 3:
        parameters['rhyme_scheme'] = sys.argv[2]
        parameters['metre'] = sys.argv[3]
    with open(sys.argv[1], 'r') as file:
        input_text = ""
        if sys.argv[1].endswith('.json'):
            # convert json to raw txt
            data = json.load(file)
            for s in range(len(data[0]["body"])):
                for l in range(len(data[0]["body"][s])):
                    input_text += data[0]["body"][s][l]["text"] + "\n"
                    input_text += "\n"
        else:
            input_text = file.read()
        try:
            results = get_measures(input_text, parameters)
        except:
            print('ERROR while processing file:', sys.argv[1], file=sys.stderr)
        
        print('Unknown words:', results['unknown_words'])
        print('Rhyming:', results['rhyming'])
        print('Rhyming accuracy:', results['rhyme_scheme_accuracy'])
        print('Rhyming consistency:', results['rhyming_consistency'])
        print('Metre accuracy:', results['metre_accuracy'])
        print('Metre consistency:', results['metre_consistency'])
        print('Syllable count entropy:', results['syllable_count_entropy'])
        print('Meaningfulness:', results['meaningfulness'])

    #print('name', 'unknown_words', 'rhyming', 'rhyme_scheme_accuracy', 'metre_consistency', 'metre_accuracy', 'syllable_count_entropy', 'rhyming_consistency', sep="\t")
    #for path in sys.argv[1:]:
    #    for filename in glob.glob(path):
    #        with open(filename, 'r') as file:
    #            input_text = ""
    #            if filename.endswith('.json'):
    #                # convert json to raw txt
    #                data = json.load(file)
    #                for s in range(len(data[0]["body"])):
    #                    for l in range(len(data[0]["body"][s])):
    #                        input_text += data[0]["body"][s][l]["text"] + "\n"
    #                    input_text += "\n"
    #            else:
    #                input_text = file.read()
    #        try:
    #            results = get_measures(input_text, {})
    #        except:
    #            print('ERROR while processing file:', filename, file=sys.stderr)
    #            raise
    #        print(filename, results['unknown_words'], results['rhyming'], results['rhyme_scheme_accuracy'], results['metre_consistency'], results['metre_accuracy'], results['syllable_count_entropy'], results['rhyming_consistency'], sep="\t")
