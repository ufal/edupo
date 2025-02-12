#!/usr/bin/env python3
#coding: utf-8

import random
import re
import sys

import logging
logging.basicConfig(
    format='%(asctime)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO)

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

import parser

MODEL_TM='/net/projects/EduPo/data/unsloth_llama_lora_002_checkpoint-15000'
MODEL_MC="jinymusim/gpt-czech-poet"

# Always load Michal's model
tokenizer_mc = AutoTokenizer.from_pretrained(MODEL_MC)
model_mc = AutoModelForCausalLM.from_pretrained(MODEL_MC)

# Try to load unsloth model
try:
    import unsloth
    from unsloth import FastLanguageModel
    model_tm, tokenizer_tm = FastLanguageModel.from_pretrained(MODEL_TM)
    FastLanguageModel.for_inference(model_tm)
except:
    logging.exception("EXCEPTION Nejde načíst unsloth model.")
    model_tm, tokenizer_tm = None, None

def _generate(poet_start, stop_strings=None, params={}):
    
    if model_tm and params['modelspec'] == 'tm':
        model = model_tm
        tokenizer = tokenizer_tm
    else:
        model = model_mc
        tokenizer = tokenizer_mc

    poet_start = poet_start.replace('<|begin_of_text|>', '')

    """
    stop_strings(`str or List[str]`, *optional*):
            A string or a list of strings that should terminate generation if the model outputs them.
    """

    # tokenize input
    tokenized_poet_start = tokenizer.encode(poet_start, return_tensors='pt').to(model.device)

    # generate a continuation to it
    out = model.generate(
            tokenized_poet_start,
            max_new_tokens=256,
            do_sample=True,
            # top_p=0.7,
            top_k=50,
            # no_repeat_ngram_size=2,
            pad_token_id= tokenizer.pad_token_id,
            temperature=params.get('temperature', 1),
            tokenizer=tokenizer,
            eos_token_id = tokenizer.eos_token_id,
            **({'stop_strings': stop_strings} if stop_strings else {}),
    )

    # decode and return
    return tokenizer.decode(out[0])
 
END_PUNCT = set(['.', '?', '!'])
def clean(verses):
    result = []
    last = '.'
    for verse in verses:
        if verse:
            if last in END_PUNCT:
                verse = verse.capitalize()
            last = verse[-1]
            result.append(verse)
    # should not end with ,
    if result[-1][-1] == ',':
        result[-1] = result[-1][:-1] + '.'

    return result

RHYME_SCHEMES = {
    4: ['ABAB', 'XXXX', 'XAXA', 'AAXX', 'AABB', 'ABBA'],
    6: ['AABBCC', 'XXXXXX', 'ABABXX', 'ABABCC'],
    }

GENERATION_PARAMS_DEFAULTS = {
    'rhyme_scheme': 'AABB',
    'metre': 'J',
    'verses_count': 4,
    'syllables_count': 8,
    'first_words': [],
    'year': 1900,
    'temperature': 1,
    'anaphors': [],
    'epanastrophes': [],
    'title': 'Bez názvu',
    'author_name': 'Vrchlický, Jaroslav',
    'max_strophes': 4,
    'modelspec': 'tm',
    }

def generuj_mc(params):

    params['modelspec'] = 'mc'

    if params.get('verses_count') not in (4, 6):
        params['verses_count'] = random.choice([4, 6])

    # TODO this now also allows thing the model cannot generate
    if not re.match(r'^[A-Z]+$', params.get('rhyme_scheme', '')):
        params['rhyme_scheme'] = random.choice(RHYME_SCHEMES[params['verses_count']])

    if not params.get('year'):
        params['year'] = '1900'

    params['verses_count'] = len(params['rhyme_scheme'])

    if not params.get('metre'):
        params['metre'] = random.choice(['J', 'T', 'D'])

    if params.get('syllables_count') not in range(1,20):
        params['syllables_count'] = random.choice(range(6, 13))

    poet_start = f"# {params['rhyme_scheme']} # {params['year']}\n"
    # D # 11 # eště # po letech v polích jsem ohlížel se ještě,
    if params.get('first_words') or params.get('anaphors') or params.get('epanastrophes'):
        first_words = params.get('first_words', [])
        anaphors = params.get('anaphors', set())
        epanastrophes = params.get('epanastrophes', set())
        assert type(first_words) == list, "first_words must be list"
        while len(first_words) < params['verses_count']:
            first_words.append('')
        while len(first_words) > params['verses_count']:
            first_words.pop()
        prev_first = ''
        prev_last = ''
        for index, word in enumerate(first_words):
            poet_start = f"{poet_start}{params['metre']} # {params['syllables_count']} #"
            # generate ending hint
            poet_start = _generate(poet_start, ' #', params)
            # anaphors and epanastrophes have precedence
            # (TODO priority, mutual exclusion)
            if index in anaphors:
                word = prev_first
            if index in epanastrophes:
                word = prev_last            
            # force word (may be empty, so what)
            poet_start = f"{poet_start} {word}"
            # generate line
            poet_start = _generate(poet_start, '\n', params)
            if index+1 in anaphors:
                prev_first = poet_start.split('#')[-1].split()[0]
            if index+1 in epanastrophes:
                prev_last = poet_start.split()[-1]
    else:
        poet_start = f"{poet_start}{params['metre']} # {params['syllables_count']} #"

    raw = _generate(poet_start, params=params)
    
    result = raw.split('<|endoftext|>')[0].split('\n')

    header = result[0]
    try:
        _, schema, year = header.split('#')
    except:
        schema = rhyme_scheme
        year = '?'
    poem = result[1:]

    for line in poem:
        try:
            meter, syls, end, verse = line.split('#')
        except:
            verse = line
        result.append(verse.strip())
    
    # TODO výhledově možná rovnou vracet v JSON formátu
    clean_verses = clean(result[-len(params['rhyme_scheme'])-1:])
    return raw, clean_verses, params.get('author_name', 'Anonym'), params.get('title', 'Bez názvu')


"""
<|begin_of_text|>Machar, Josef Svatopluk: V lese (1932)

# A B A B #
# T # 8 # uky # Jaká vůně! Jaké zvuky!
# T # 8 # ízy # Padají ty světlé mízy!
# T # 8 # uky # Opony padají s buky!
# T # 8 # yzy # Zří v tvé duše všecky hryzy!

# A B A B #
# T # 8 # anou # Časem pod tvou drsnou blanou
# T # 8 # yla # zlaťoučká se slupka skryla –
# T # 8 # anou # – Nadagrams oblohou stanou,
# T # 8 # ila # bozi, která zapálila! –
<|end_of_text|>

"""

def generuj_tm(params):

    params['modelspec'] = 'tm'
    
    poem = ''
    
    # preamble

    author_name = params.get('author_name')
    if not author_name:
        author_name = GENERATION_PARAMS_DEFAULTS['author_name']
    # TODO random select
    poem += f"{author_name}:"

    if params.get('title'):
        poem += f" {params['title']} ("
    else:
        poem = _generate(poem, '(', params)

    if params.get('year'):
        poem += f"params['{year}'])\n"
    else:
        poem = _generate(poem, '\n', params)
    
    poem += "\n#"

    # strophes
    strophes = 0
    while strophes < params.get('max_strophes', 4) and '<|end_of_text|>' not in poem:
        if params.get('rhyme_scheme'):
            rhyme_scheme_tm = " ".join(list(params['rhyme_scheme'].replace("X", "x")))
            poem += f" {rhyme_scheme_tm} #\n"
        else:
            poem = _generate(poem, '\n', params)
        
        try:
            verses_count = len(poem.split('\n')[-2].split('#')[1].split())
        except:
            verses_count = len(params.get('rhyme_scheme', 'AABB'))

        # verses
        for _ in range(verses_count):
            if params.get('metre'):
                poem += f"# {params['metre']} #"
            else:
                poem = _generate(poem, '#', params)

            if params.get('syllables_count'):
                poem += f" {params['syllables_count']} #"
            else:
                poem = _generate(poem, '#', params)

            # reduplicant
            poem = _generate(poem, '#', params)

            if params.get('first_words'):
                word = params['first_words'].pop(0)
                poem += f" {word} "
                # TODO anaphors and epanastrophes
            poem = _generate(poem, '\n', params)

        # end of strophe
        # (generate empty line or end of text)
        poem = _generate(poem, '\n', params)
        strophes += 1
        
    # parse result
    result = poem.split('<|end_of_text|>')[0].split('\n')
    header = result[0]
    lines = result[2:]
    
    # header
    try:
        m = re.match(r'^<\|begin_of_text\|>([^:]*): (.*) \(([^()]*)\)$', header)
        # m = re.match(r'^([^:]*): (.*) \(([^()]*)\)$', header)
        author_name, title, year = m.groups()
    except:
        author_name = params.get('author_name', 'Anonym')
        title = params.get('title', 'Bez názvu')
        title = params.get('year', '?')

    # verses
    verses = []
    for line in lines:
        verses.append(line.split('#')[-1].strip())
    
    return poem, verses, author_name, title

def generuj(params):
    if model_tm and params.get('modelspec') == 'tm':
        return generuj_tm(params)
    else:
        return generuj_mc(params)


if __name__=="__main__":
    try:
        rhyme_scheme = sys.argv[1]
    except:
        rhyme_scheme = 'AABB'

    result = generuj({
        'modelspec': 'tm',
        'rhyme_scheme': rhyme_scheme,
        })
    print(*result, sep='\n')
