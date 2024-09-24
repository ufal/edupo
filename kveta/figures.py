import re
import math
import pprint
import json
import os

class Figures:
    
    
    def __init__(self):
        '''
        Initialize Figures
        '''
    def analyze(self, poem):
        '''
        Analyze figures
        '''

        for i, line in enumerate(poem):

            narrators_gender = ""

            for word1 in line['words']:
                if word1['morph'][0] == 'V' and word1['morph'][7] == '1' and word1['morph'][3] == 'S': # pokud je to sloveso v první osobě singuláru
                    for word2 in line['words']:
                        if word1['parent'] == word2['tok_id']:
                            if word2['morph'][2] in ['M','Y']:
                                narrators_gender = "M"
                            elif word2['morph'][2] in ['F','H']:
                                narrators_gender = "F"
                        elif word1['tok_id'] == word2['parent'] and word2['morph'][4] == '1':
                            if word2['morph'][2] in ['M','Y','Z']:
                                narrators_gender = "M"
                            elif word2['morph'][2] in ['F','H','Q']:
                                narrators_gender = "F"

            if narrators_gender:
                poem[i]['narrators_gender'] = narrators_gender

        return poem

            
