from ufal.morphodita import *
import re

class Morphodita:
    
    
    def __init__(self):
        '''
        Initialize MorphoDiTa
        '''
        
        self.tagger = Tagger.load('dicts/czech-morfflex-pdt-161115.tagger')
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
                
                # If token is a punctuation mark store it as attribute of 
                # previous word (if any)
                if lemma.tag.startswith('Z'):
                    if len(poem[l]['words']) > 0:
                        poem[l]['words'][-1]['punct'] = text[token.start : token.start + token.length]                

                # ...otherwise append token tags to current line
                else:
                    poem[l]['words'].append({
                        'token': text[token.start : token.start + token.length],
                        'lemma': re.sub('\-.*$|\:.*$| *\^.*$| *;.*$|\,.*$', '', lemma.lemma),
                        'morph': lemma.tag,
                        'sentence': s,
                    })
                    
                # If token followed by <newline>: increase the line index
                if (len(text) >= token.start + token.length + 1
                and text[token.start + token.length] == '\n'):
                    l += 1

                # Increase token index
                t = token.start + token.length

            # Increase sentence index
            s += 1
            
        return poem

