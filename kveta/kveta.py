#!/usr/bin/python3

import sys
import json
import preprocessing
import morph
import phonetix
import line2vec
import syllables
import meter
import rhyme
import pprint
import json
import operator
import htmlprint
from collections import defaultdict


class Kveta:
    
    def __init__(self, text):
        self.text_ = text
        
    def preprocessing(self):
        self.poem_ = preprocessing.stanza_separator(self.text_)
        
    def pos_tagging(self):
        mdt = morph.Morphodita()
        self.poem_ = mdt.tag(self.poem_)
        
    def phonetics(self):
        ptx = phonetix.Phonetix()
        self.poem_ = ptx.transcript_poem(self.poem_)     
    def syllables(self):
        syl = syllables.Syllables()
        self.poem_ = syl.split_words_to_syllables(self.poem_)
    def line2vec(self):
        l2v = line2vec.Line2Vec()
        self.poem_ = l2v.tag(self.poem_)

    def meter(self):
        mtr = meter.Meter(dt=False)
        self.poem_, self.overall_probs_ = mtr.analyze(self.poem_)
        
    def rhyme(self, rwindow, rpsounds, rpngrams):
        rt = rhyme.RhymeDetection(window=rwindow, probability_sampa_min=rpsounds, probability_ngram_min=rpngrams)
        self.poem_ = rt.tag(self.poem_)

    def htmlprint(self, mscore=0.5):
        html = htmlprint.HTMLprint()
        self.html_, self.pie_data_ = html.stringify(self.poem_, self.overall_probs_, mscore)


def okvetuj(text):
    # Get parameters

    k = Kveta(text)
    k.preprocessing()
    k.pos_tagging()
    k.phonetics()
    k.syllables()
    k.line2vec()
    k.meter()
    #k.rhyme(rwindow, rpsounds, rpngrams)
    k.rhyme(6, 0.95, 0.95)
    #k.htmlprint(mscore)
    k.htmlprint()


    #output = {
    #    'pie_data': k.pie_data_,
    #    'object': {
    #        'metres': k.overall_probs_,
    #        'poem': k.poem_,
    #    },
    #}

    # Change the rhyming format to CCV style
    #rc = dict()
    #cur_num = 0
    #for i, v in enumerate(k.poem_):
    #    minimum = i
    #    for x in v["rhyme"]:
    #        if x < minimum:
    #            minimum = x
    #    if not minimum in rc:
    #        cur_num += 1
    #        rc[minimum] = cur_num
    #    k.poem_[i]["rhyme"] = rc[minimum]

    # Change the rhyming format to CCV style
    minimum2cluster = dict()
    rhyme_clusters = []
    for i, v in enumerate(k.poem_):
        minimum = i
        for x in v["rhyme"]:
            if x < minimum:
                minimum = x
        if not minimum in minimum2cluster:
            minimum2cluster[minimum] = len(rhyme_clusters)
            rhyme_clusters.append([i])
        else:
            rhyme_clusters[minimum2cluster[minimum]].append(i)
        k.poem_[i]["rhyme"] = minimum2cluster[minimum] + 1

    # Fill rhyme_from attribute - values 'v' (from vovel), 'c' (from consonants), 'ec' (from the ending consonants)
    for c in rhyme_clusters:
        if len(c) == 1:
            # no rhyming
            # TODO: jak to má v tomto případě vypadat?
            jenabytunecobylo = 1
        else:
            for l in c:
                if len(k.poem_[l]["words"][-1]["syllables"]) >= 2: # víceslabičné slovo
                    k.poem_[l]["words"][-1]["syllables"][-2]["rhyme_from"] = 'v'
                    k.poem_[l]["words"][-1]["syllables"][-1]["rhyme_from"] = 'c'
                elif len(k.poem_[l]["words"]) >= 2 and k.poem_[l]["words"][-2]["vec"] and k.poem_[l]["words"][-2]["vec"]["prep"][0] == 1: # jednoslabičné slovo za slabičkou předložkou
                    k.poem_[l]["words"][-1]["syllables"][-1]["rhyme_from"] = 'c'
                    k.poem_[l]["words"][-2]["syllables"][-1]["rhyme_from"] = 'v'
                elif k.poem_[l]["words"][-1]["syllables"][-1]["ph_end_consonants"]: # jednoslabičné slovo bez předložky končící souhláskou
                    k.poem_[l]["words"][-1]["syllables"][-1]["rhyme_from"] = 'v'
                else:
                    k.poem_[l]["words"][-1]["syllables"][-1]["rhyme_from"] = 'c' # jednoslabičné slovo bez předložky končící samohláskou
            # TODO: co když jsou v rámci klastru některá slova jednoslabičná a některá např. tříslabičná?



    # Put metres from k.pie_data_ into verses
    for i, v in enumerate(k.poem_):
        letter = "T"
        #if k.pie_data_[i]["metre"] == "iamb":
        #    letter = "J"
        #elif k.pie_data_[i]["metre"] == "dactyl":
        #    letter = "D"
        #TODO: Tady se to musí vyřešit líp. Podle KCV tu má bejt dict s klíči, T, J, D, ... ale blbě se s tim pak bude pracovat. Zatim tam dávám všude T
        k.poem_[i]["metre"] = [ {letter: k.pie_data_[i]} ]


    # Change the JSON structure to resemble CCV
    output = [
        { 
            "metres": k.overall_probs_,
            "body": [ k.poem_ ]
        }
    ]

    # Copy the streses and S/W/V into indivisual syllables
    for i, v in enumerate(k.poem_):
        swv = v["metre"][0]["T"]["pattern"]
        stress = v["sections"]
        pointer = 0
        for j, w in enumerate(v["words"]):
            for l, s in enumerate(w["syllables"]):
                k.poem_[i]["words"][j]["syllables"][l]["position"] = swv[pointer]
                k.poem_[i]["words"][j]["syllables"][l]["stress"] = stress[pointer]
                pointer += 1

    return output, k


if __name__=="__main__":
    filename = sys.argv[1]

    # read poem
    text = ""
    with open(filename) as f:
        for line in f:
            text += line
    f.close()

    # run Kveta
    output, k = okvetuj(text)
    
    # write output
    if filename[-4:] == ".txt":
        filename = filename[:-4]

    with open(filename+'.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
    f.close()

    with open(filename+'.html', 'w', encoding='utf-8') as h:
        h.write(k.html_)
    h.close()


