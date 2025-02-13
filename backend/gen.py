#!/usr/bin/env python3
#coding: utf-8

import sys

import logging
logging.basicConfig(
    format='%(asctime)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO)

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import random
import re

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

def _generate(poet_start,
        stop_strings=None,
        temperature=1,
        modelspec='tm'):
    
    if model_tm and modelspec=='tm':
        model = model_tm
        tokenizer = tokenizer_tm
    else:
        model = model_mc
        tokenizer = tokenizer_mc

    poet_start = poet_start.replace('<|begin_of_text|>', '')

    """
    stop_strings(`str or List[str]`, *optional*):
            A string or a list of strings that should terminate generation if the model outputs them.
            The original implementation did not work for me, so I did my own
            with eos_token_id, but this requires the stop_strings to be full
            tokens (so e.g. ' #' instead of just '#').
    """

    # tokenize input
    tokenized_poet_start = tokenizer.encode(poet_start, return_tensors='pt').to(model.device)

    if stop_strings:
        if isinstance(stop_strings, str):
            stop_strings = [stop_strings]
        assert isinstance(stop_strings, list)
    else:
        stop_strings = []

    # generated a continuation to it
    out = model.generate(
            tokenized_poet_start,
            max_new_tokens=256,
            do_sample=True,
            # top_p=0.7,
            top_k=50,
            # no_repeat_ngram_size=2,
            pad_token_id= tokenizer.pad_token_id,
            stop_strings = stop_strings,
            temperature=temperature,
            )

    # Decode Poet
    result = tokenizer.decode(out[0])
    
    return result

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

def generuj_mc(rhyme_scheme='AABB', metre='J', verses_count=0, syllables_count=0,
        first_words=[], first_line='', year=1900, temperature=1,
        anaphors=[], epanastrophes=[], title='', author_name=''):
    # TODO probably refactor into parameters as a dict?

    if verses_count not in (4, 6):
        verses_count = random.choice([4, 6])

    # TODO this now also allows thing the model cannot generate
    if not re.match(r'^[A-Z]+$', rhyme_scheme):
        rhyme_scheme = random.choice(RHYME_SCHEMES[verses_count])

    if not year:
        year = '1900'

    # this is probably not needed here unless verses_count is used for something
    verses_count = len(rhyme_scheme)

    if not metre:
        metre = random.choice(['J', 'T', 'D'])

    if syllables_count not in range(1,20):
        syllables_count = random.choice(range(6, 13))

    poet_start = f'# {rhyme_scheme} # {year}\n'
    # D # 11 # eště # po letech v polích jsem ohlížel se ještě,
    if first_line:
        # !! TODO fix this !!
        ending_hint = first_line[:3]  
        # !! TODO set syllables_count properly !!
        poet_start = f"{poet_start}{metre} # {syllables_count} # {ending_hint} # {first_line}\n"
    elif first_words or anaphors or epanastrophes:
        assert type(first_words) == list, "first_words must be list"
        while len(first_words) < verses_count:
            first_words.append('')
        while len(first_words) > verses_count:
            first_words.pop()
        prev_first = ''
        prev_last = ''
        for index, word in enumerate(first_words):
            poet_start = f'{poet_start}{metre} # {syllables_count} #'
            # generate ending hint
            poet_start = _generate(poet_start, '#', temperature, 'mc')
            # anaphors and epanastrophes have precedence
            # (TODO priority, mutual exclusion)
            if index in anaphors:
                word = prev_first
            if index in epanastrophes:
                word = prev_last            
            # force word (may be empty, so what)
            poet_start = f"{poet_start} {word}"
            # generate line
            poet_start = _generate(poet_start, '\n', temperature, 'mc')
            if index+1 in anaphors:
                prev_first = poet_start.split('#')[-1].split()[0]
            if index+1 in epanastrophes:
                prev_last = poet_start.split()[-1]
    else:
        poet_start = f'{poet_start}{metre} # {syllables_count} #'

    raw = _generate(poet_start, [], temperature, 'mc')
    
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
    clean_verses = clean(result[-len(rhyme_scheme)-1:])
    author_name = author_name if author_name else 'Anonym'
    title = title if title else 'Bez názvu'
    return raw, clean_verses, author_name, title


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

def generuj_tm(rhyme_scheme='AABB', metre=None, verses_count=0, syllables_count=0,
        first_words=[], first_line='', year=None, temperature=1,
        anaphors=[], epanastrophes=[], title='', author_name='',
        max_strophes=4):
    # TODO probably refactor into parameters as a dict?

    # poem = '<|begin_of_text|>'
    poem = ''
    
    # preamble
    if author_name:
        poem += f" {author_name}:"
    else:
        # TODO random select
        poem += "Rosa, Rudolf:"
        # poem = _generate(poem, ':', temperature)

    if title:
        poem += f" {title} ("
    else:
        poem = _generate(poem, '(', temperature)

    if year:
        poem += f"{year})\n"
    else:
        poem = _generate(poem, '\n', temperature)
    
    poem += "\n#"

    # strophes
    strophes = 0
    stop = False
    while strophes < max_strophes and '<|end_of_text|>' not in poem:
        if rhyme_scheme:
            rhyme_scheme_tm = " ".join(list(rhyme_scheme.replace("X", "x")))
            poem += f" {rhyme_scheme_tm} #\n"
        else:
            poem = _generate(poem, '\n', temperature)
        
        try:
            verses_count = len(poem.split('\n')[-2].split('#')[1].split())
        except:
            verses_count = len(rhyme_scheme)

        # verses
        for _ in range(verses_count):
            if metre:
                poem += f"# {metre} #"
            else:
                poem = _generate(poem, '#', temperature)

            if syllables_count:
                poem += f" {syllables_count} #"
            else:
                poem = _generate(poem, '#', temperature)

            # reduplicant
            poem = _generate(poem, '#', temperature)

            if first_words:
                word = first_words.pop(0)
                poem += f" {word} "
                # TODO anaphors and epanastrophes
            poem = _generate(poem, '\n', temperature)

        # end of strophe
        # (generate empty line or end of text)
        poem = _generate(poem, '\n', temperature)
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
        author_name = author_name if author_name else 'Anonym'
        title = title if title else 'Bez názvu'
        year = year if year else '?'

    # verses
    verses = []
    for line in lines:
        verses.append(line.split('#')[-1].strip())
    
    return poem, verses, author_name, title

def generuj(rhyme_scheme='AABB', metre=None, verses_count=0, syllables_count=0,
        first_words=[], first_line='', year=None, temperature=1,
        anaphors=[], epanastrophes=[], title='', author_name='',
        max_strophes=4, modelspec='tm'):

    if model_tm and modelspec == 'tm':
        return generuj_tm(rhyme_scheme, metre, verses_count, syllables_count,
            first_words, first_line, year, temperature,
            anaphors, epanastrophes, title, author_name,
            max_strophes)
    else:
        return generuj_mc(rhyme_scheme, metre, verses_count, syllables_count,
            first_words, first_line, year, temperature,
            anaphors, epanastrophes, title, author_name)


if __name__=="__main__":
    try:
        rhyme_scheme = sys.argv[1]
    except:
        rhyme_scheme = 'AABB'

    result = generuj(rhyme_scheme)
    print(*result, sep='\n')
