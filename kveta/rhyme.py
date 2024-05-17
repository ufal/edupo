import re
from rhymeTagger import RhymeTagger

class RhymeDetection:
    
    
    def __init__(self, window=6, probability_sampa_min=0.95, probability_ngram_min=0.95):
        '''
        Initialize RhymeTagger
        '''
        
        self.tagger = RhymeTagger(stanza_limit=False, stress=True, ngram=True, 
                                  window=window, 
                                  probability_sampa_min=probability_sampa_min, 
                                  probability_ngram_min=probability_ngram_min)
        self.tagger.load_model(model='trained_models/rhymes.json')
       

    def tag(self, poem):
        '''
        Perform tagging
        '''

        fin_words = []
        for l in poem:
            xsampa = self.cft_to_xsampa(l['words'][-1]['cft'])
            
            # přidální případné předchozí slabičné předložky
            if len(l['words']) >=2 and l['words'][-2]["vec"] and l['words'][-2]["vec"]["prep"][0] == 1:
                xsampa = self.cft_to_xsampa(l['words'][-2]['cft']) + xsampa

            if l['words'][-1]['morph'][0] in ('N','A','D','V','C') and l['words'][-1]['lemma'] != 'být':
                xsampa = "'" + xsampa
            fin_words.append({'word': l['words'][-1]['token'],
                              'sampa': xsampa,
                              'stanza': l['stanza']})

        r = self.tagger.tagging(fin_words)
        
        for i,l in enumerate(poem):
            poem[i]['rhyme'] = list(r[i])
        return poem  
            

    def cft_to_xsampa(self, cft):

        ct = self.conversion_table()

        xsampa = ''
        for p in cft:
            xsampa += ct[p]
        return xsampa

    def conversion_table(self):        

        return {
            'a': 'a', 
            'e': 'e',
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
        }
