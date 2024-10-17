import re
import math
import pprint
import json
import os

class Meter:
    
    
    def __init__(self, dt=True, sub=True):
        '''
        Initialize Line2Vec
        '''

        self.dt_ = dt
        self.sub_ = sub
        self.feet_ = ('SW', 'SWW')
    

    def analyze(self, poem, model='random_forest.json'):
        '''
        Analyze meters
        '''
        filepath = os.path.join(os.path.dirname(__file__),
                'trained_models', model)

        self.poem_ = poem
        self._g_component()
        overall_probs = self._m_component(filepath)

        return self.poem_, overall_probs


    def _g_component(self):
        '''
        Generate metrical patterns        
        '''
        
        # Get longest line
        longest = max([len(l['sections']) for l in self.poem_])

        # Create container for patterns
        self.patterns_ = set()
        
        # Generate all possible patterns
        if self.dt_:
            # Downward patterns
            self._generator(self.feet_, longest, '')
            # Upward patterns
            self._generator(self.feet_, longest, 'W')

        # Generate binary and ternary meters
        else:
            self.patterns_ = {
                ('WS' * math.ceil(longest/2))[0:longest],        
                ('SW' * math.ceil(longest/2))[0:longest],
                ('SWW' * math.ceil(longest/3))[0:longest],
                ('WSW' * math.ceil(longest/3))[0:longest],
            }


    def _generator(self, feet, length, init_piece):
        '''
        Recursive function to produce all possible combinations
        of SW/SWW + anacrusis + male ending
        '''
    
        if len(init_piece) == length-1:
            self.patterns_.add(init_piece+'S')
        if len(init_piece) == length:
            self.patterns_.add(init_piece)
        if len(init_piece) >= length:
            return
    
        for f in feet:
           self._generator(feet, length, init_piece+f)           


    def _m_component(self, model):
        '''
        Probabilities of metrical patterns
        '''
        
        with open(model) as f:
            probs = json.load(f)
            
        overall_probs = dict()
        for pattern in self.patterns_:    
            overall_probs[pattern] = 1

        for i,line in enumerate(self.poem_):
            self.poem_[i]['metre'] = dict()

            # Defaultní distribuce pro čtyři základní metra
            self.poem_[i]['metre_probs'] = {'T': 00.1, 'J': 0.01, 'D': 0.01, 'A':0.01 }

            for pattern in self.patterns_:    
                self.poem_[i]['metre'][pattern] = 1
                position = 0

                for w in line['words']:
    
                    if len(w['vec']) == 0:
                        continue
    
                    for j,x in enumerate(w['vec']['prevInit']):
    
                        vec = [
                            w['vec']['prevInit'][j],
                            w['vec']['nextLong'][j],
                            w['vec']['prevPrep'][j],
                            w['vec']['content'][j],
                            w['vec']['lengths'][j],
                            w['vec']['final'][j],
                            w['vec']['initial'][j],
                        ]            
    
                        key = ''.join("{0}".format(n) for n in vec)
                        if pattern[position] == 'W' and position == 0:
                            position += 1
                            continue
                        self.poem_[i]['metre'][pattern] *= probs[key][pattern[position]]
                        position += 1
                        
                self.poem_[i]['metre'][pattern] = self.poem_[i]['metre'][pattern] ** (1/len(pattern))
                overall_probs[pattern] *= self.poem_[i]['metre'][pattern]

                # Vyplň distribuce pro čtyři základní metra
                if pattern.startswith('SWW'):
                    self.poem_[i]['metre_probs']['D'] = self.poem_[i]['metre'][pattern]
                elif pattern.startswith('WSWW'):
                    self.poem_[i]['metre_probs']['A'] = self.poem_[i]['metre'][pattern]
                elif pattern.startswith('SW'):
                    self.poem_[i]['metre_probs']['T'] = self.poem_[i]['metre'][pattern]
                elif pattern.startswith('WS'):
                    self.poem_[i]['metre_probs']['J'] = self.poem_[i]['metre'][pattern]

            # Normalizace 'metre_probs'
            total = 0
            for M in ['T', 'J', 'D', 'A']:
                total += self.poem_[i]['metre_probs'][M]
            for M in ['T', 'J', 'D', 'A']:
                self.poem_[i]['metre_probs'][M] /= total

        for m in overall_probs:
            overall_probs[m] = overall_probs[m] ** (1/len(self.poem_))
        return overall_probs

            
