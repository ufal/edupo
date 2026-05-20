import re
from rhymeTagger import RhymeTagger
import os
import sys

class RhymeDetection:
    
    
    def __init__(self, window=6, probability_sampa_min=0.95, probability_ngram_min=0.95):
        '''
        Initialize RhymeTagger
        '''
        
        self.tagger = RhymeTagger(stanza_limit=False, stress=True, ngram=True, 
                                  window=window, 
                                  probability_sampa_min=probability_sampa_min, 
                                  probability_ngram_min=probability_ngram_min)
        

        filepath = os.path.join(os.path.dirname(__file__),
                'trained_models', 'rhymes.json')
        self.tagger.load_model(model=filepath)
       

    def tag(self, poem):
        '''
        Perform tagging
        '''

        fin_words = []
        for l in poem:
            if l['words']:
                xsampa = self.cft_to_xsampa(l['words'][-1]['cft'])
            
                # přidální případné předchozí neslabičné nebo slabičné předložky
                if len(l['words']) >=2 and (l['words'][-2]['token'] in ['s', 'z', 'v', 'k'] and l['words'][-2]['morph'][0] == 'R' or l['words'][-2]["vec"] and l['words'][-2]["vec"]["prep"][0] == 1):
                    xsampa = self.cft_to_xsampa(l['words'][-2]['cft']) + xsampa

                if l['words'][-1]['morph'][0] in ('N','A','D','V','C') and l['words'][-1]['lemma'] != 'být':
                    xsampa = "'" + xsampa
                fin_words.append({'word': l['words'][-1]['token'],
                                  'sampa': xsampa,
                                  'stanza': l['stanza']})
            else:
                fin_words.append({'word': 'xxxxx', 'sampa': 'xxxxx', 'stanza': l['stanza']})

        r = self.tagger.tagging(fin_words)

        # Change the rhyming format to CCV style
        minimum2cluster = dict()
        rhyme_clusters = []
        for i, v in enumerate(poem):
            minimum = i
            for x in r[i]:
                if x < minimum:
                    minimum = x
            if not minimum in minimum2cluster:
               minimum2cluster[minimum] = len(rhyme_clusters)
               rhyme_clusters.append([i])
            else:
               rhyme_clusters[minimum2cluster[minimum]].append(i)

        # do "rhyme" u veršů vyplníme číslo klastru
        cluster_number = 0
        for c in rhyme_clusters:
            if len(c) == 1:
                # no rhyming
                poem[c[0]]["rhyme"] = None 
            else:
                cluster_number += 1
                for l in c:
                    if not poem[l]["words"]:
                        poem[l]["rhyme"] = None
                    else:
                        poem[l]["rhyme"] = cluster_number
        return poem

    def mark_reduplicants(self, poem):

        rhyme_clusters = dict()
        for i, l in enumerate(poem):
            if poem[i]["rhyme"]:
                rhymeID = poem[i]["rhyme"]
                if not rhymeID in rhyme_clusters:
                    rhyme_clusters[rhymeID] = [i]
                else:
                    rhyme_clusters[rhymeID].append(i)

        # do "rhyme_from" u slabik vyplníme od které pozice se rýmují, možné hodnoty: 'v' (from vovel), 'c' (from consonants), 'ec' (from the ending consonants)
        for c in rhyme_clusters:
            # nejdřív otestujeme, jestli se v klastru nachází jednoslabičné slovo (bez předložky)
            exists_monosyllabic_word = 0
            for l in rhyme_clusters[c]:
                if poem[l]["words"] and len(poem[l]["words"][-1]["syllables"]) == 1 and (len(poem[l]["words"]) == 1 or (poem[l]["words"][-2]["morph"][0] != 'R' and poem[l]["words"][-2]["syllables"])):
                    exists_monosyllabic_word = 1
                    break
            # nyní označujeme začátky rýmujících se částí
            for l in rhyme_clusters[c]:
                if not poem[l]["words"][-1]["syllables"]:
                    # poslední slovo je neslabičné
                    print("INFO: the last word in line is non-syllabic", file=sys.stderr)
                elif not exists_monosyllabic_word and len(poem[l]["words"][-1]["syllables"]) >= 2: # víceslabičné slovo
                    poem[l]["words"][-1]["syllables"][-2]["rhyme_from"] = 'v'
                    poem[l]["words"][-1]["syllables"][-1]["rhyme_from"] = 'c'
                elif not exists_monosyllabic_word and len(poem[l]["words"]) >= 2 and poem[l]["words"][-2]["morph"][0] == 'R' and poem[l]["words"][-2]["syllables"]: # jednoslabičné slovo za slabičkou předložkou
                    poem[l]["words"][-1]["syllables"][-1]["rhyme_from"] = 'c'
                    poem[l]["words"][-2]["syllables"][-1]["rhyme_from"] = 'v'
                elif poem[l]["words"][-1]["syllables"][-1]["ph_end_consonants"]: # jednoslabičné slovo bez předložky končící souhláskou
                    poem[l]["words"][-1]["syllables"][-1]["rhyme_from"] = 'v'
                else:
                    poem[l]["words"][-1]["syllables"][-1]["rhyme_from"] = 'c' # jednoslabičné slovo bez předložky končící samohláskou
        return poem  
            

    def cft_to_xsampa(self, cft):

        ct = self.conversion_table()

        xsampa = ''
        for p in cft:
            if p in ct:
                xsampa += ct[p]
            else:
                print('Unknown character', p, file=sys.stderr)
        return xsampa

    def conversion_table(self):        

        return {
            'a': 'a', 
            'e': 'E',
            'i': 'I',
            'o': 'o',
            'u': 'u',

            'á': 'a:', 
            'é': 'E:',
            'í': 'i:',
            'ó': 'o:',
            'ú': 'u:',
        
            'A': 'a_u', 
            'E': 'e_u',
            'O': 'o_u',

            'R': 'r=',        
            'L': 'l=',       
            'P': 'm=',
            'B': 'n=',
        
            'p': 'p',        
            'b': 'b',        
            't': 't',        
            'd': 'd',        
            'ť': 'c',        
            'ď': 'J!',        
            'k': 'k',        
            'g': 'g',        

            'f': 'f',        
            'v': 'v',        
            's': 's',        
            'z': 'z',        
            'š': 'S',        
            'ž': 'Z',        
            'x': 'x',        
            'X': '',        
            'h': 'h\\',        
            'G': 'g',        

            'c': 't_s',        
            'č': 't_S',        

            'm': 'm',        
            'n': 'n',        
            'ň': 'N',   
            'V': 'm',        
            'W': 'n',              
            'Z': 'c',
            'Ž': 'č',

            'r': 'r',        
            'l': 'l',        
            'j': 'j',        
            'ř': 'P\\',        
            'Ř': 'Q\\',

            '@': '@',
        }
