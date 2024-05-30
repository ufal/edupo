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
    
    def phoebe2cft(self):
        ptx = phonetix.Phonetix()
        self.poem_ = ptx.phoebe2cft(self.poem_)     
    
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

    def read_ccv(self, data):
        # sesypej strofy do jednoho pole a přidej atribut stanza
        self.poem_ = []
        for i, stanza in enumerate(data):
            print(stanza)
            for line in stanza:
                line["stanza"] = i
                self.poem_.append(line)

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


    # Change the JSON structure to resemble CCV
    output = [
        { 
            "metres": k.overall_probs_,
            "body": [ k.poem_ ]
        }
    ]

    # Put metres from k.pie_data_ into verses
    # and copy the streses and S/W/V into individual syllables
    for i, v in enumerate(k.poem_):
        letter = "N"
        if k.pie_data_[i]["metre"] == "trochee":
            letter = "T"
        elif k.pie_data_[i]["metre"] == "iamb":
            letter = "J"
        elif k.pie_data_[i]["metre"] == "dactyl":
            letter = "D"
        k.poem_[i]["metre"] = [ {letter: k.pie_data_[i]} ]
        
        swv = v["metre"][0][letter]["pattern"]
        stress = v["sections"]
        pointer = 0
        for j, w in enumerate(v["words"]):
            for l, s in enumerate(w["syllables"]):
                k.poem_[i]["words"][j]["syllables"][l]["position"] = swv[pointer]
                k.poem_[i]["words"][j]["syllables"][l]["stress"] = stress[pointer]
                pointer += 1

    return output, k

def okvetuj_ccv(data):

    k = Kveta("")
    k.read_ccv(data)
    k.phoebe2cft()
    k.syllables()

    data = k.poem_

    return data


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


