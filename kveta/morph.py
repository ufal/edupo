from ufal.morphodita import *
import re
import os

class Morphodita:
    
    
    def __init__(self):
        '''
        Initialize MorphoDiTa
        '''
        
        filepath = os.path.join(os.path.dirname(__file__),
                'dicts', 'czech-morfflex-pdt-161115.tagger')
        self.tagger = Tagger.load(filepath)
        self.forms = Forms()
        self.lemmas = TaggedLemmas()
        self.tokens = TokenRanges()
        self.tokenizer = self.tagger.newTokenizer()

    def tag(self, poem):
        '''
        Perform POS-tagging and lemmatization of the text
        '''

        # Merge lines of poem with <newline>
        text = '\n'.join([x['text'] for x in poem])

        # Pass poem to tokenizer
        self.tokenizer.setText(text)

        # Line index
        l = 0        
        # Token index
        t = 0
        # Sentence index
        s = 0

        # Iterate over sentences
        while self.tokenizer.nextSentence(self.forms, self.tokens):
            self.tagger.tag(self.forms, self.lemmas)

            # Iterate over tokens
            for i in range(len(self.lemmas)):
                lemma = self.lemmas[i]
                token = self.tokens[i]

                str_lemma = re.sub(r'\-.*$|\:.*$| *\^.*$| *;.*$|\,.*$', '', lemma.lemma)
                str_token = text[token.start : token.start + token.length]


                # TODO: mark non-diphtong candidates
                nodip = ""
                nodip_prefixes = ["anglo", "bystro", "celo", "dlouho", "dobro", "do", "eko", "kraso", "krátko", "indo", "jedno", "jiho", "lehko", "makro", "malo", "mikro", "mnoho", "mravo", "nízko", "novo", "polo", "pro", "po", "prvo", "pseudo", "rychlo", "samo", "severo", "sladko", "staro", "sto", "středo", "těžko", "velko", "věro", "vnitro", "východo", "vysoko", "západo", "zlato", "zlo"]
                nodip_nolemma_suffixes = ["uchý", "učka", "učkově", "učkový", "učně", "učný", "učovat", "uk", "uka", "ukově", "ukový"]
                for prefix in nodip_prefixes:
                    if str_lemma.startswith(prefix+'u'):
                        suffix = str_lemma[len(prefix):]
                        if len(suffix) <= 1:
                            continue
                        # tag the suffix
                        forms2 = Forms()
                        lemmas2 = TaggedLemmas()
                        tokens2 = TokenRanges()
                        tokenizer2 = self.tagger.newTokenizer()
                        tokenizer2.setText(suffix)
                        tokenizer2.nextSentence(forms2,tokens2)
                        self.tagger.tag(forms2,lemmas2,0) # The last argument is 0 since we don't want to use morphological guesser.
                        # if suffix was not recognized by the tagger (tag X) or suffix is in the list
                        if lemmas2[0].tag[0] != 'X' or suffix in nodip_nolemma_suffixes:
                            print(suffix, lemmas2[0].tag)
                            p = str_token.find(prefix) + len(prefix)
                            nodip = str_token[:p] + '₇' + str_token[p:] # ₇ is used here as a sign in places where ou is not a diphtong
                            #print("SUCCESS", nodip)
                        break

                # If token is a punctuation mark store it as attribute of 
                # previous word (if any)
                if lemma.tag.startswith('Z'):
                    if len(poem[l]['words']) > 0:
                        poem[l]['words'][-1]['punct'] = text[token.start : token.start + token.length]


                # ...otherwise append token tags to current line
                else:                    features = {'token': str_token,
                                'lemma': str_lemma,
                                'morph': lemma.tag,
                                'sentence': s
                                }
                    if nodip:
                        features['nodip'] = nodip
                    poem[l]['words'].append(features)
                    
                # If token followed by <newline>: increase the line index
                if (len(text) >= token.start + token.length + 1
                and text[token.start + token.length] == '\n'):
                    l += 1

                # Increase token index
                t = token.start + token.length

            # Increase sentence index
            s += 1
            
        return poem

