#from ufal.morphodita import *
import re
import os
import sys
import requests

sys.path.append(os.path.abspath('../scripts/diphthongs'))
from hyphenator import Hyphenator

class Morphodita:
    
    
    def __init__(self):

        # initialize Hyphenator for detecting diphthongs
        with open("../scripts/diphthongs/diphthongs.patterns", 'r') as f:
            patterns = f.read().splitlines()
        self.hyp = Hyphenator(patterns)

    def tag(self, poem):
        '''
        Perform POS-tagging and lemmatization of the text
        '''

        # Merge lines of poem with <newline>
        text = '\n'.join([x['text'] for x in poem]) + '\n'

        # perform the UDPipe request to parse the whole poem
        response = requests.get("https://lindat.mff.cuni.cz/services/udpipe/api/process?tokenizer=ranges&tagger&parser&data=" + text)

        l = 0 # line index
        t = 0 # token index
        s = 0 # sentence index
        
        for line in response.json()["result"].split("\n"):
            sent_id = re.match("^# sent_id = (\d+)", line)
            if sent_id:
                s = sent_id.groups()[0]
            if line and line[0].isdigit():
                items = line.split("\t")
                
                # If token is a punctuation mark (tag starts with Z) store it as attribute of previous word (if any)
                if items[4].startswith('Z'):
                    if len(poem[l]['words']) > 0:
                        poem[l]['words'][-1]['punct'] = items[1]

                # ...otherwise append token tags to current line
                else:
                    features = {'token': items[1],
                                'lemma': items[2],
                                'morph': items[4],
                                'tok_id': items[0],
                                'parent': items[6],
                                'deprel': items[7],
                                'sentence': s
                                }
                    # mark non-diphtongs candidates using Tomáš's Hyphenator
                    segments = self.hyp.hyphenate_word(items[1].lower())
                    if len(segments) > 1:
                        features['nodip'] = '₇'.join(segments)
                    
                    poem[l]['words'].append(features)
                
                    
                # If the token is followed by a newline (e.g. TokenRange=45:49 and there is a newline on the position 49), increase the line index
                if text[int(items[9].split(":")[-1])] == '\n':
                    l += 1
            
        return poem

