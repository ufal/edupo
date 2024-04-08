import operator
from collections import defaultdict

class HTMLprint:
    
    
    def __init__(self):
        '''
        Initialize class
        '''
       

    def stringify(self, poem, overall_probs, mscore):
        '''
        Strongify results
        '''
        
        self.poem_ = poem
        self.overall_probs_ = overall_probs
        pie_data = []

        meter = max(self.overall_probs_.items(), key=operator.itemgetter(1))[0] 
        if self.overall_probs_[meter] <= mscore:
            meter = 'X' * len(meter)
        
        output = defaultdict(lambda: defaultdict(dict))
        
        count_rhymes = 0;

        for i,l in enumerate(self.poem_):

            syll = 0
            output[i]['rhyme'][0] = ' '.join("#{0}".format(n+1) for n in l['rhyme'])
            
            for r in l['rhyme']:
                if r < i:
                    count_rhymes += 1

            for j,w in enumerate(l['words']):

                output[i]['token'][j] = w['token']
                output[i]['lemma'][j] = w['lemma']
                output[i]['morph'][j] = w['morph']
                output[i]['cft'][j] = w['cft']
                if len(w['vec']) == 0:
                    output[i]['rhythm'][j] = ''
                    output[i]['meter'][j] = ''                    
                else:
                    output[i]['rhythm'][j] = l['sections'][syll:syll+len(w['vec']['content'])]
                    output[i]['meter'][j] = meter[syll:syll+len(w['vec']['content'])]
                    syll += len(w['vec']['content'])

        self.html_ = '<div id="kveta-stats"><div id="kveta-stats-head">STATS</div>'

        first = True;
        metre_winner = ''

        for m in sorted(self.overall_probs_, key=self.overall_probs_.get, reverse=True):
            
            if m.startswith('WSWW'):
                metre = 'amphibrach'
            elif m.startswith('SWW'):
                metre = 'dactyl'
            elif m.startswith('SW'):
                metre = 'trochee'
            else:
                metre = 'iamb'

            if first and self.overall_probs_[m] <= mscore:
                self.html_ += '<div class="kveta-stats-item kveta-stats-item-winner">'
                self.html_ += 'unknown'.format(metre, round(self.overall_probs_[m], 4))
                self.html_ += '</div>'
                self.html_ += '<div class="kveta-stats-item">'
                self.html_ += '{0} (m-score = {1})'.format(metre, round(self.overall_probs_[m], 4))
                self.html_ += '</div>'
                metre_winner = 'unknown'
                
            elif first and self.overall_probs_[m] > mscore:
                self.html_ += '<div class="kveta-stats-item kveta-stats-item-winner">'
                self.html_ += '{0} (m-score = {1})'.format(metre, round(self.overall_probs_[m], 4))
                self.html_ += '</div>'
                metre_winner = metre
                
            else:                
                self.html_ += '<div class="kveta-stats-item">'
                self.html_ += '{0} (m-score = {1})'.format(metre, round(self.overall_probs_[m], 4))
                self.html_ += '</div>'
                
            first = False
        self.html_ += '<div class="kveta-stats-rhyme"># rhymes: {0}</div>'.format(count_rhymes)
        self.html_ += '</div>'
        
        for i,l in enumerate(self.poem_):
            

            pattern = ''.join(output[i]['meter'].values())
            if metre_winner != 'unkown':
                foot = pattern.count('S')
                if pattern.endswith('SWW'):
                    clause = 'a'
                elif pattern.endswith('SW'):
                    clause = 'f'
                else:
                    clause = 'm'
                metre_winner_name = '{0}-{1}-{2}'.format(metre_winner, foot, clause)
                pie_data.append({
                    'pattern': pattern,
                    'metre': metre_winner,
                    'foot': foot,
                    'clause': clause,
                    'full': metre_winner_name,
                })
            else:
                pie_data.append({
                    'pattern': pattern,
                    'metre': metre_winner,
                    'foot': 0,
                    'clause': 'n',
                    'full': metre_winner,
                })
            
            
            if i > 0 and l['stanza'] != self.poem_[i-1]['stanza']:
                self.html_ += '<table class="lineAnnot newStanza">'
            else:
                self.html_ += '<table class="lineAnnot">'

            self.html_ += '<tr><td>#{0}</td></tr>'.format(i+1)

            for x in ('token', 'meter', 'rhythm', 'rhyme', 'lemma', 'morph'):
                self.html_ += '<tr class="lineAnnot-{0}"><td></td><td class="lineAnnot-label">{0}:</td>'.format(x)
                for j in output[i][x]:
                    self.html_ += '<td>{0}</td>'.format(output[i][x][j])
                if x == 'meter':
                    self.html_ += '<td>({0})</td>'.format(metre_winner_name)
                self.html_ += '</tr>'
        
            self.html_ += '</table>'
            
        return self.html_, pie_data