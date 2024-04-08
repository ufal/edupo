import re

def poem_separator(text, sep='###poem###'):
    '''
    Split input text into poems according to selected separator
    '''
    
    poems = text.split(sep)
    return poems


def stanza_separator(text):
    '''
    Split poem into stanzas (list of lists)    
    '''
    
    # Remove the rubbish
    text = _clean_text(text)
    # Split text into stanzas
    stanzas = text.split('\n\n')
    # Split stanzas into lines and create a poem object
    poem_obj = list()
    for i,x in enumerate(stanzas):
        stanzas[i] = stanzas[i].split('\n')
        for y in stanzas[i]:
            poem_obj.append({
                'text': y.strip(),
                'stanza': i,
                'words': list(),
            })

    return poem_obj


def _clean_text(text):
    '''
    Remove rubbish from the poem
    '''

    # Unify newline symbol
    text = re.sub('\r', '\n', text)
    # Remove numbers
    text = re.sub('[0-9]+', ' ', text)
    # Replace tabs with blankspace
    text = re.sub('\t', ' ', text)
    # Replace whitespaces neighbouring with newline
    text = re.sub('\n +| +\n', '\n', text)
    # Remove multiple consecutive whitespaces    
    text = re.sub(' +', ' ', text)
    # More then 2 consequent newlines → 2 newlines
    text = re.sub('\n\n+', '\n\n', text)
    # Delete text initial and text final newlines
    text = re.sub('^\n+|\n+$', '', text)
    
    return text
    