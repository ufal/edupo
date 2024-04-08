#!/usr/bin/python3

import cgi, cgitb 
import json
import preprocessing
import morph
import phonetix
import line2vec
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



# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get parameters

text = form.getvalue('t')
mscore = float(form.getvalue('m'))
rwindow = int(form.getvalue('w'))
rpsounds = float(form.getvalue('s'))
rpngrams = float(form.getvalue('g'))

k = Kveta(text)
k.preprocessing()
k.pos_tagging()
k.phonetics()
k.line2vec()
k.meter()
k.rhyme(rwindow, rpsounds, rpngrams)
k.htmlprint(mscore)


output = {
    'html': k.html_,
    'pie_data': k.pie_data_,
    'object': {
        'metres': k.overall_probs_,
        'poem': k.poem_,
    },
}


print ("Content-type:json\n\n")
print (json.dumps(output))
