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
import figures
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
        self.poem_ = rt.mark_reduplicants(self.poem_)

    def reduplicants(self):
        rt = rhyme.RhymeDetection()
        self.poem_ = rt.mark_reduplicants(self.poem_)
        
    def figures(self):
        fig = figures.Figures()
        self.poem_ = fig.analyze(self.poem_)

    def htmlprint(self, mscore=0.5):
        html = htmlprint.HTMLprint()
        self.html_, self.pie_data_ = html.stringify(self.poem_, self.overall_probs_, mscore)

    def read_ccv(self, data):
        self.poem_ = data

        # move punctuation from verse to words
        for i, verse in enumerate(self.poem_):
            pos = 0
            word_index = 0
            corrupted_word = False
            while word_index < len(verse['words']) and pos <= len(verse['text']):
                current_word = verse['words'][word_index]['token']
                current_punct = ""
                while pos+len(current_word) <= len(verse['text']) and current_word != verse['text'][pos:pos+len(current_word)] and current_word != verse['text'][pos:pos+len(current_word)+1].replace('’','').replace("'","") and (not verse['text'][pos].isalpha() or corrupted_word):
                    current_punct += verse['text'][pos]
                    if corrupted_word and verse['text'][pos].isalpha():
                        current_punct = ""
                    pos += 1
                if current_word == verse['text'][pos:pos+len(current_word)+1].replace('’','').replace("'",""):
                    current_word = verse['text'][pos:pos+len(current_word)+1]
                    self.poem_[i]['words'][word_index]['token'] = current_word
                    corrupted_word = False
                elif current_word == verse['text'][pos:pos+len(current_word)]:
                    corrupted_word = False
                elif verse['text'][pos].isalpha():
                    # nasledujici slovo v textu neodpovida nasledujicimu tokenu
                    # preskoc tenhle token a vypis interpunkci
                    corrupted_word = True
                if word_index == 0:
                    self.poem_[i]['words'][0]['punct_before'] = current_punct
                else:
                    self.poem_[i]['words'][word_index - 1]['punct'] = current_punct
                if not corrupted_word:
                    pos += len(current_word)
                word_index += 1
            if not corrupted_word and pos < len(verse['text']):
                self.poem_[i]['words'][-1]['punct'] = verse['text'][pos:]
        #del verse['punct']

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
    k.figures()
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
            "body": k.poem_
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
        elif k.pie_data_[i]["metre"] == "amphibrach":
            letter = "A"
        k.poem_[i]["metre"] = {letter: k.pie_data_[i]} 
        
    return output, k

def okvetuj_ccv(data):


    k = Kveta("")
    k.read_ccv(data)
    k.phoebe2cft()
    k.syllables()
    k.reduplicants()
    
    # k.figures()
    # line 26 KeyError parent

    data = k.poem_

    return data


if __name__=="__main__":
    
    filename = sys.argv[1]
    print("Processing", filename, file=sys.stderr)

    # read poem
    text = ""
    if filename.endswith(".txt"):
        with open(filename) as f:
            for line in f:
                text += line
        f.close()
    elif filename.endswith(".json"):
        f = open(filename)
        data = json.load(f)
        for i in range(len(data[0]["body"])):
            for j in range(len(data[0]["body"][i])):
                text += data[0]["body"][i][j]["text"] + "\n"
            text += "\n"
        f.close()
    else:
        print("Only TXT and JSON formats are supported.", file=sys.stderr)

    # run Kveta
    output, k = okvetuj(text)

    if len(sys.argv) > 2:
        output_filename = sys.argv[2]
    elif filename.endswith(".txt"):
        output_filename = filename[:-3] + "json"

    print("Writing to", output_filename, file=sys.stderr)
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
    f.close()

