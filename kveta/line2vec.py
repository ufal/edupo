import re

class Line2Vec:
    
    def __init__(self):
        '''
        Initialize Line2Vec
        '''
        pass

    def tag(self, poem):
        '''
        
        '''

        self.poem_ = poem


        for i, l in enumerate(self.poem_):
            
            self.line_vec = dict()
            
            for j, w in enumerate(l['words']):
                
                lengths = self._lengths(w['cft'])
                initial, final = self._positions(lengths)
                content = self._content(lengths, w['morph'], w['lemma'])
                prep = self._prepositions(lengths, w['morph'], w['token'])

                if len(lengths) == 0:
                    self.poem_[i]['words'][j]['vec'] = {}
                    continue
                self.poem_[i]['words'][j]['vec'] = {
                    'lengths': lengths,     
                    'initial': initial,
                    'final': final,
                    'content': content,
                    'prep': prep
                }
            
                self._prev_prep(i, j)
                self._prev_init(i, j)
            self._next_long(i)
            self._stress(i)
            

        return self.poem_
    

    def _lengths(self, cft):
        '''
        Assign syllable attrobute long/short
        '''
        
        lengths = list()

        for s in cft:
            if s in ('á', 'é', 'í', 'ó', 'ú', 'A', 'O', 'E'):
                lengths.append(1)
            if s in ('a', 'e', 'i', 'o', 'u', 'R', 'L', 'M', 'N'):
                lengths.append(0)

        return lengths
                

    def _positions(self, lengths):
        '''
        Assign syllable attributes word-initial / word-final
        '''
        
        initial = [ 1 ] + (len(lengths) - 1) * [0]
        final = (len(lengths) - 1) * [0] + [1]
        return initial, final
        
    
    def _content(self, lengths, morph, lemma):
        '''
        Assign syllable attributes content-word / function-word
        '''
        
        if  ( morph[0] in ('N','A','C','V','D','I')
        and ( lemma != 'být' or morph[0] != 'V') ):
            return len(lengths) * [1]
        else:
            return len(lengths) * [0]
        
        
    def _prepositions(self, lengths, morph, token):
        '''
        Annotate monosyllabic prepositions proper
        '''
       
        mpps = ('před','od','ob','ku','ke','do','ve','pod','nad','přes',
                'při','bez','se','ze','za','u','pod','pro','zpod', 'o', 'po', 
                'na')       
       
        if token.lower() in mpps and morph[0] == 'R':
            return len(lengths) * [1]
        else:
            return len(lengths) * [0]
        
        
    def _prev_prep(self, i, j):
        '''
        Annotate whether preceded by a preposition
        '''
        
        lengths = self.poem_[i]['words'][j]['vec']['lengths']

        if j == 0:
            self.poem_[i]['words'][j]['vec']['prevPrep'] = len(lengths) * [0]    
        else:

            if ( 
                len(self.poem_[i]['words'][j-1]['vec']) != 0 and
                self.poem_[i]['words'][j-1]['vec']['prep'][-1] == 1
            ):
                self.poem_[i]['words'][j]['vec']['prevPrep'] = [ 1 ] + (len(lengths) - 1) * [0]

            elif (
                len(self.poem_[i]['words'][j-1]['vec']) == 0 and
                j > 1 and
                len(self.poem_[i]['words'][j-2]['vec']) != 0 and
                self.poem_[i]['words'][j-2]['vec']['prep'][-1] == 1            
            ):
                self.poem_[i]['words'][j]['vec']['prevPrep'] = [ 1 ] + (len(lengths) - 1) * [0]

            else:
                self.poem_[i]['words'][j]['vec']['prevPrep'] = len(lengths) * [0]


    def _prev_init(self, i, j):
        '''
        Annotate whether preceded by a word-initial syllable
        '''

        lengths = self.poem_[i]['words'][j]['vec']['lengths']

        for k, z in enumerate(lengths):
            if k == 0:
                if j == 0:
                    self.poem_[i]['words'][j]['vec']['prevInit'] = [0]
                elif ( 
                    len(self.poem_[i]['words'][j-1]['vec']) != 0 and
                    self.poem_[i]['words'][j-1]['vec']['initial'][-1] == 1 
                ):
                    self.poem_[i]['words'][j]['vec']['prevInit'] = [1]
                elif (
                    len(self.poem_[i]['words'][j-1]['vec']) == 0 and
                    j > 1 and
                    len(self.poem_[i]['words'][j-2]['vec']) != 0 and
                    self.poem_[i]['words'][j-2]['vec']['initial'][-1] == 1
                ):                
                    self.poem_[i]['words'][j]['vec']['prevInit'] = [1]
                else:
                    self.poem_[i]['words'][j]['vec']['prevInit'] = [0]
            else:
                if self.poem_[i]['words'][j]['vec']['initial'][k-1] == 1:
                    self.poem_[i]['words'][j]['vec']['prevInit'].append(1)
                else:
                    self.poem_[i]['words'][j]['vec']['prevInit'].append(0)
                
      
    def _next_long(self, i):      
        '''
        Annotate whether followed by a long syllable
        '''
        
        for j, w in enumerate(self.poem_[i]['words']):

            if len(w['vec']) == 0:
                continue

            nextlong = len(w['vec']['lengths']) * [0]
            
            for k, z in enumerate(nextlong):                                
                if k >= len(nextlong) - 1:
                    if j >= len(self.poem_[i]['words']) - 1:
                        nextlong[k] = 0
                    elif (
                        len(self.poem_[i]['words'][j+1]['vec']) != 0 and
                        self.poem_[i]['words'][j+1]['vec']['lengths'][0] == 1
                    ):
                        nextlong[k] = 1                        
                    elif (
                        len(self.poem_[i]['words'][j+1]['vec']) == 0 and
                        j < len(self.poem_[i]['words']) - 2 and
                        len(self.poem_[i]['words'][j+2]['vec']) != 0 and
                        self.poem_[i]['words'][j+2]['vec']['lengths'][0] == 1
                    ):                                        
                        nextlong[k] = 1
                    else:
                        nextlong[k] = 0
                else:
                    if w['vec']['lengths'][k+1] == 1:
                        nextlong[k] = 1
                    else:
                        nextlong[k] = 0

            self.poem_[i]['words'][j]['vec']['nextLong'] = nextlong
            

    def _stress(self, i):
        '''
        Generate R-sections
        '''
        
        sections = str()
        for j, w in enumerate(self.poem_[i]['words']):
            
            if len(w['vec']) == 0:
                continue


            if w['vec']['prep'][0] == 1:
                sections += 'R'
            elif len(w['vec']['lengths']) > 1:
                sections += '1' + '0' * (len(w['vec']['lengths']) - 1)
            elif ( j == 0 
            or    ('punct' in self.poem_[i]['words'][j-1]
            and    re.search(r'[\.\;\?\!\,\-\–]', self.poem_[i]['words'][j-1]['punct']))):
                sections += 'n'
            else:
                if w['vec']['content'][0] == 1:
                    sections += 'M'
                else:
                    sections += 'm'
                    
        sections = re.sub('R1', '10', sections)
        sections = re.sub('RM', '1m', sections)
        sections = re.sub('R0', '10', sections)
        sections = re.sub('R', '0', sections)
        
        sections = re.sub('nm', '10', sections)
        sections = re.sub('n', '0', sections)
        sections = re.sub('m', '0', sections)
        sections = re.sub('M', '1', sections)
        sections = re.sub('N', '1', sections)
                    
        self.poem_[i]['sections'] = sections
                                       

        
        
        
        
