from ufal.morphodita import *
import re
import os
import sys
import requests
import json
import time

sys.path.append(os.path.abspath('../scripts/diphthongs'))
from hyphenator import Hyphenator

class Morphodita:
    
    
    def __init__(self):
        '''
        Initialize MorphoDiTa
        '''
        
        filepath = os.path.join(os.path.dirname(__file__),
                'dicts', 'czech-morfflex-pdt-161115.tagger')
        filepath_morpho = os.path.join(os.path.dirname(__file__),
                'dicts', 'czech-morfflex-161115.dict')
        self.tagger = Tagger.load(filepath)
        self.morpho = Morpho.load(filepath_morpho)
        self.forms = Forms()
        self.lemmas = TaggedLemmas()
        self.tokens = TokenRanges()
        self.tokenizer = self.tagger.newTokenizer()
        
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


        # Pass poem to tokenizer
        self.tokenizer.setText(text)

        vertical_input = ""
        newline_after = []
        
        # Iterate over sentences
        while self.tokenizer.nextSentence(self.forms, self.tokens):

            for i, t in enumerate(self.tokens):

                # create vertical input for UDPipe
                vertical_input += text[t.start : t.start + t.length] + "\n"
                if text[t.start + t.length] == "\n":
                    newline_after.append(True)
                else:
                    newline_after.append(False)
            vertical_input += "\n"

        # perform the UDPipe request to parse the whole poem
        api_data = {"tagger": True, "parser": True, "model": "czech-fictree-ud-2.12-230717", "input": "vertical", "data": vertical_input}
        response = requests.post("https://lindat.mff.cuni.cz/services/udpipe/api/process", api_data)
        
        #try:
        #    response.json()
        #except (RuntimeError, TypeError, NameError):
        #    print(response)

        # sometimes more attempts are needed to get the output from the UDPipe
        if not response:
            for attempt in range(5):
                time.sleep(3)
                print("No result from UDPipe. Making another request.", file=sys.stderr)
                response = requests.post("https://lindat.mff.cuni.cz/services/udpipe/api/process", api_data)
                if response:
                    break

        l = 0 # line index
        t = 0 # token index
        s = 0 # sentence index

        initial_punctuation = ""

        for line in response.json()["result"].split("\n"):
            sent_id = re.match("^# sent_id = (\\d+)", line)
            if sent_id:
                s = sent_id.groups()[0]
            if line and line[0].isdigit():
                items = line.split("\t")
                # if token is a punctuation mark, store it as the 'punct' attribute of the previous word or punc_before attribute of the next word
                if items[4][0] == 'Z' or (len(items[1]) == 1 and not items[1][0].isalnum()): #items[1][0] in '‛’‘–”“„‚*<>{}()[]'
                    if len(poem[l]['words']) > 0:
                        if 'punct' in poem[l]['words'][-1]:
                            poem[l]['words'][-1]['punct'] += " " + items[1]
                        else:
                            poem[l]['words'][-1]['punct'] = items[1]
                    else:
                        initial_punctuation += items[1]
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
                    # include the initial punctuation if exists
                    if initial_punctuation:
                        features['punct_before'] = initial_punctuation
                        initial_punctuation = ""

                    # mark non-diphtongs candidates using Tomáš's Hyphenator
                    segments = self.hyp.hyphenate_word(items[1].lower())
                    if len(segments) > 1:
                        features['nodip'] = '₇'.join(segments)

                    # is the word included in the MorphoDita dictionary?
                    result = self.morpho.analyze(features['token'], self.morpho.GUESSER, self.lemmas)
                    if result == self.morpho.GUESSER:
                        features['is_unknown'] = True
                    
                    poem[l]['words'].append(features)

                    # the atribut pnct must be filled
                    if not poem[l]['words'][-1]['punct']:
                        poem[l]['words'][-1]['punct'] = " "

                if newline_after[t]:
                    l += 1
                t += 1

        return poem

