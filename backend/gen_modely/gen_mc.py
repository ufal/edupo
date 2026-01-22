import logging
import random
import re

import parsy
from transformers import AutoModelForCausalLM, AutoTokenizer

import parser


MODEL="jinymusim/gpt-czech-poet"

def load_model(modelspec=None):

    logging.info(f"Loading model {modelspec} {MODEL}")

    # load Michal's model
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForCausalLM.from_pretrained(MODEL)
    with open('prompt_templates/chudoba.txt', 'r') as f:
        template = parser.Template(f.read())

    logging.info("Model loaded: " + modelspec)
    return model, tokenizer, template

# default parameter values
DEFAULT = {
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
    'max_strophes': 2,
    'modelspec': 'tm',
    }

RHYME_SCHEMES = {
    4: ['ABAB', 'XXXX', 'XAXA', 'AAXX', 'AABB', 'ABBA'],
    6: ['AABBCC', 'XXXXXX', 'ABABXX', 'ABABCC'],
    }

def set_default_if_not(params, key):
    if not params.get(key, None):
        params[key] = DEFAULT[key]

"""
# ABAB # 1900
D # 8 # ází #  proč tam ten černý tam mlází,
D # 8 # emi #  a teď v té zatmělé zemi
D # 8 # ází #  snad ještě něco přichází
D # 8 # emi #  a teď tam ti mrtví všemi!
<|endoftext|>
"""

def generuj(gen, template, params):

    params['modelspec'] = 'mc'

    if params.get('verses_count') not in (4, 6):
        params['verses_count'] = random.choice([4, 6])

    # TODO this now also allows thing the model cannot generate
    if not re.match(r'^[A-Z]+$', params.get('rhyme_scheme', '')):
        params['rhyme_scheme'] = random.choice(RHYME_SCHEMES[params['verses_count']])

    set_default_if_not(params, 'year')

    params['verses_count'] = len(params['rhyme_scheme'])

    if not params.get('metre'):
        params['metre'] = random.choice(['J', 'T', 'D'])

    if params.get('syllables_count') not in range(1,20):
        params['syllables_count'] = random.choice(range(6, 13))


    # ABAB # 1900
    poet_start = f"# {params['rhyme_scheme']} # {params['year']}\n"
    if 'interactive_mode' in params:
        userinput = params['userinput'].strip()
        if not params['rawtext']:
            # starting generation
            poet_start = f"{poet_start}{params['metre']} # {params['syllables_count']} #"
            if params['interactive_mode'].endswith('hg'):
                # user already started
                if params['interactive_mode'].startswith('lines'):
                    # full line from user: get user reduplicant
                    reduplicant = userinput[-3:]
                    poet_start += f" {reduplicant} # {userinput}\n{params['metre']} # {params['syllables_count']} #"
                    raw, generated = gen(poet_start, '\n')
                else:
                    # finish the user line: invent reduplicant and generate
                    poet_start, generated = gen(poet_start, '#')
                    poet_start += f" {userinput}"
                    raw, generated = gen(poet_start, '\n')
            else:
                # generator starts
                raw, generated = gen(poet_start, '\n')
                if params['interactive_mode'].startswith('verses'):
                    # cut off second half
                    tokens = generated.split('#')[-1].split()
                    part = (len(tokens) + 1) // 2
                    continuation = " ".join(tokens[:part])
                    raw = f"{poet_start} <REDUPLICANT> # {continuation}"
        else:
            # continuing generation: add userinput to rawtext and continue
            if params['interactive_mode'].startswith('lines'):
                poet_start = f"{params['rawtext'].strip()}\n{params['metre']} # {params['syllables_count']} #"
                # full line from user: get user reduplicant
                reduplicant = userinput[-3:]
                poet_start += f" {reduplicant} # {userinput}\n{params['metre']} # {params['syllables_count']} #"
                raw, generated = gen(poet_start, '\n')
            else:
                if params['interactive_mode'].endswith('hg'):
                    poet_start = f"{params['rawtext'].strip()}\n{params['metre']} # {params['syllables_count']} #"
                    # finish the user line: invent reduplicant and generate
                    poet_start, generated = gen(poet_start, '#')
                    poet_start += f" {userinput}"
                    raw, generated = gen(poet_start, '\n')
                else:
                    # fill reduplicant in last line
                    reduplicant = params['userinput'].strip()[-3:]
                    poet_start = params['rawtext'].replace('<REDUPLICANT>', reduplicant).strip()
                    poet_start += f" {params['userinput'].strip()}\n{params['metre']} # {params['syllables_count']} #"

                    # we start the line
                    raw, generated = gen(poet_start, '\n')
                    # cut off second half
                    tokens = generated.split('#')[-1].split()
                    part = (len(tokens) + 1) // 2
                    continuation = " ".join(tokens[:part])
                    raw = f"{poet_start} <REDUPLICANT> # {continuation}"


    elif params.get('first_words') or params.get('anaphors') or params.get('epanastrophes'):
        first_words = params.get('first_words', [])
        anaphors = params.get('anaphors', set())
        epanastrophes = params.get('epanastrophes', set())
        assert isinstance(first_words, list), "first_words must be list"
        while len(first_words) < params['verses_count']:
            first_words.append('')
        while len(first_words) > params['verses_count']:
            first_words.pop()
        prev_first = ''
        prev_last = ''
        for index, word in enumerate(first_words):
            # D # 11 # eště # po letech v polích jsem ohlížel se ještě,
            poet_start = f"{poet_start}{params['metre']} # {params['syllables_count']} #"
            # generate ending hint
            poet_start, generated = gen(poet_start, ' #')
            # anaphors and epanastrophes have precedence
            # (TODO priority, mutual exclusion)
            if index in anaphors:
                word = prev_first
            if index in epanastrophes:
                word = prev_last            
            # force word (may be empty, so what)
            poet_start = f"{poet_start} {word}"
            # generate line
            poet_start, generated = gen(poet_start, '\n')
            if index+1 in anaphors:
                prev_first = poet_start.split('#')[-1].split()[0]
            if index+1 in epanastrophes:
                prev_last = poet_start.split()[-1]
        # generate till the end of the poem
        raw, generated = gen(poet_start)
    else:
        # generate the poem at once
        poet_start = f"{poet_start}{params['metre']} # {params['syllables_count']} #"
        raw, generated = gen(poet_start)
    
    result = raw.split('<|endoftext|>')[0]

    END_PUNCT = set(['.', '?', '!'])
    def clean(verses):
        result = []
        last = '.'
        for verse in verses:
            if verse:
                verse = verse.strip()
                if last in END_PUNCT:
                    verse = verse.capitalize()
                last = verse[-1]
                result.append(verse)
        # should not end with ,
        if result[-1][-1] == ',':
            result[-1] = result[-1][:-1] + '.'

        return result

    try:
        parsed = (parsy.string('<|begin_of_text|>').optional()
                  >> template.poem_parser()).parse(result + '\n\n') # TODO fix hack with \n\n
        result = [v['line'] for v in parsed['verses']]
        clean_verses = clean(result)
    except parsy.ParseError as e:
        logging.warning("WARNING Nepodařený parsing básně: " + str(e))
        header = result[0]

        result = result.split('\n')
        try:
            _, params['rhyme_scheme'], params['year'] = header.split('#')
        except:
            set_default_if_not(params, 'rhyme_scheme')
            params['year'] = '?'
        poem = result[1:]

        for line in poem:
            try:
                meter, syls, end, verse = line.split('#')
            except:
                verse = line
            result.append(verse.strip())

        # TODO výhledově možná rovnou vracet v JSON formátu
        clean_verses = clean(result)
    return raw, clean_verses, params.get('author_name', 'Anonym'), params.get('title', DEFAULT['title'])
