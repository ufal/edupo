import logging
import random
import re
from functools import reduce

import parsy
import torch
from unsloth import FastLanguageModel

import parser

MODEL='/net/projects/EduPo/data/unsloth_llama_lora_002_checkpoint-7500'

def load_model(modelspec=None, load16bit=True, **kwargs):

    logging.info(f"Loading model {modelspec} {MODEL}")

    kwargs = {}
    if load16bit:
        kwargs['dtype'] = torch.bfloat16
        kwargs['load_in_4bit'] = False
    else:
        kwargs['load_in_4bit'] = True
        logging.info("Loading in 4bit.")
    model, tokenizer = FastLanguageModel.from_pretrained(
        MODEL,
        **kwargs,
        )
    FastLanguageModel.for_inference(model)

    with open('prompt_templates/tm1.txt', 'r') as f:
        template = parser.Template(f.read())

    #logging.info(f"model_tm: {model_tm}")
    #logging.info(f"tokenizer_tm: {tokenizer_tm}")

    logging.info("Model loaded: " + modelspec)
    return model, tokenizer, template

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

AUTHORS = open('authors', 'r').read().splitlines()

def generuj(gen, template, params_orig):

    params = params_orig.copy() # TODO fix this ugly hack

    poem = ''

    # preamble

    if not params.get('author_name'): #TODO `params` readonly
        params['author_name'] = random.choice(AUTHORS)
    poem += f"{params['author_name']}:"

    if params.get('title'):
        poem += f" {params['title']} ("
    else:
        poem, generated = gen(poem, '(', krok='title')

    if params.get('year'):
        poem += f"{params['year']})\n"
    else:
        poem, generated = gen(poem, ')\n', krok='year')

    # strophes
    strophes = 0
    max_len_strophe = 16
    while strophes < params.get('max_strophes', 2) and '<|end_of_text|>' not in poem:
        poem += "#"
        if params.get('rhyme_scheme'):
            if ' ' in params['rhyme_scheme']:
                # multischeme poem (such as sonet)
                rhyme_scheme_parts = params['rhyme_scheme'].split(' ')
                stanza_rhyme_scheme = rhyme_scheme_parts[strophes % len(rhyme_scheme_parts)]
            else:
                stanza_rhyme_scheme = params['rhyme_scheme']
            rhyme_scheme_tm = " ".join(list(stanza_rhyme_scheme.replace("X", "x")))
            poem += f" {rhyme_scheme_tm} #\n"
        else:
            _, generated = gen(poem, '\n', krok='rhyme_scheme')
            if len(generated.split()) > max_len_strophe + 1:
                generated = ' ' + ' '.join(generated.split()[:max_len_strophe]) + ' #\n'
            poem += generated

        try:
            verses_count = len(poem.split('\n')[-2].split('#')[1].split())
        except:
            verses_count = len(params.get('rhyme_scheme', 'AABB'))

        # verses
        for verse_index in range(verses_count):
            generated = ''

            # metre
            if params.get('metre'):
                poem += f"# {params['metre']} #"
            else:
                poem, generated = gen(poem + '#', '#', krok='metre')

            if '\n' in generated:
                poem = '\n'.join(poem.split('\n')[:-1]) + '\n'
                if params.get('first_words'):
                    params['first_words'].pop(0)
                continue

            # syllables count
            if params.get('syllables_count'):
                if isinstance(params['syllables_count'], int):
                    syllcount = params['syllables_count']
                else:
                    assert isinstance(params['syllables_count'], list)
                    syllcount = params['syllables_count'][verse_index % len(params['syllables_count'])]
                poem += f" {syllcount} #"
            else:
                poem, generated = gen(poem, '#', krok='syllables_count')

            if '\n' in generated:
                poem = '\n'.join(poem.split('\n')[:-1]) + '\n'
                if params.get('first_words'):
                    params['first_words'].pop(0)
                continue

            # reduplicant
            poem, generated = gen(poem, '#', krok='reduplicant')

            if '\n' in generated:
                poem = '\n'.join(poem.split('\n')[:-1]) + '\n'
                if params.get('first_words'):
                    params['first_words'].pop(0)
                continue

            # generate line
            if params.get('first_words'):
                word = params['first_words'].pop(0) # TODO readonly
                if word:
                    poem += f" {word}"
                # TODO anaphors and epanastrophes
            poem, generated = gen(poem, '\n', krok='verse')

        # end of strophe
        # (generate empty line or end of text)
        # poem, generated = _generate(poem, '\n', params)
        if poem[-2:] != '\n\n':
            poem += '\n'
        strophes += 1

    # parse result
    result = poem.split('<|end_of_text|>')[0]

    try:
        parsed = (parsy.string('<|begin_of_text|>').optional()
                  >> template.poem_parser()).parse(result + '\n\n') # TODO fix hack with \n\n

        author_name = parsed.get('author_name')
        title = parsed.get('poem_title')
        verses = reduce(lambda x, y: x + [''] + y,
                        [[v['line'] for v in s['verses']] for s in parsed['stanzas']])

    except parsy.ParseError as e:
        logging.warning("EXCEPTION Nepodařený parsing básně:" + str(e))

        result = result.split('\n')
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
            #year = params.get('year', '?')

        # verses
        verses = []
        for line in lines:
            verses.append(line.split('#')[-1].strip())

    return poem, verses, author_name, title