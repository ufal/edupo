#!/usr/bin/env python3
#coding: utf-8

import argparse
from functools import reduce
import random
import re
import json

import logging

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import parsy

import parser

logging.basicConfig(
    format='%(levelname)s %(asctime)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO)

MODEL_TM='/net/projects/EduPo/data/unsloth_llama_lora_002_checkpoint-15000'
MODEL_MC="jinymusim/gpt-czech-poet"

VERBOSE_INFO=False
LOAD16BIT=False
NOSAMPLE=False

RHYME_SCHEMES = {
    4: ['ABAB', 'XXXX', 'XAXA', 'AAXX', 'AABB', 'ABBA'],
    6: ['AABBCC', 'XXXXXX', 'ABABXX', 'ABABCC'],
    }

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

AUTHORS = open('authors', 'r').read().splitlines()

def load_models(modelspec=None):

    logging.info(f"Loading model {modelspec} {MODEL_TM if modelspec == 'tm' else MODEL_MC}")

    if modelspec == 'mc':
        # load Michal's model
        tokenizer = AutoTokenizer.from_pretrained(MODEL_MC)
        model = AutoModelForCausalLM.from_pretrained(MODEL_MC)
        with open('prompt_templates/chudoba.txt', 'r') as f:
            template = parser.Template(f.read())


    elif modelspec == 'tm':
        import unsloth
        from unsloth import FastLanguageModel
        kwargs = {}
        if LOAD16BIT:
            kwargs['dtype'] = torch.bfloat16
            kwargs['load_in_4bit'] = False
        else:
            kwargs['load_in_4bit'] = True
            logging.info("Loading in 4bit.")
        model, tokenizer = FastLanguageModel.from_pretrained(
            MODEL_TM,
            **kwargs,
            )
        FastLanguageModel.for_inference(model)
        with open('prompt_templates/tm1.txt', 'r') as f:
            template = parser.Template(f.read())

        #logging.info(f"model_tm: {model_tm}")
        #logging.info(f"tokenizer_tm: {tokenizer_tm}")
    else:
        logging.exception("EXCEPTION Nebyl vybrán model.")


    logging.info("Model loaded.")
    return model, tokenizer, template

def _show_tokenization(tokenizer, tokens):
    return ('|' + '|'.join(tokenizer.convert_ids_to_tokens(tokens)
                   ).replace('Ġ', ' '
                            ).replace('Ċ', '↲\n'
                            ).replace('Ã½', 'ý'
                            ).replace('ÃŃ', 'í'
                            ).replace('ÄĽ', 'ě'
                            ).replace('Ã¡', 'á'
                            ).replace('Å¡', 'š'
                            ).replace('Äį', 'č'
                            ).replace('Ãģ', 'Á'
                            ).replace('ÅĪ', 'ň'
                            ).replace('âĢĻ', '’'
                            ).replace('ÅĻ', 'ř'
                            ).replace('Å¾', 'ž'
                            ).replace('Ãº', 'ú'
                            ).replace('Ã©', 'é'
                            ).replace('Å¥', 'ť'
                            ).replace('Ãį', 'Í'
                            ).replace('Å¯', 'ů'
                            ).replace('Åĺ', 'Ř'
                            ).replace('ÄĮ', 'Č'
                            ).replace('Åł', 'Š'
                            ).replace('âĢĵ', '–'
                            )
            + '|')

def _generate(model, tokenizer, temperature=1):
    def g(poet_start, stop_strings=None, krok=None):
        """
        stop_strings(`str or List[str]`, *optional*):
                A string or a list of strings that should terminate generation if the model outputs them.
        """

        if not model or not tokenizer:
            logging.error('No model loaded, cannot generate!')
            raise Exception('No model loaded, cannot generate!')

        poet_start = poet_start.replace('<|begin_of_text|>', '')

        # tokenize input
        tokenized_poet_start = tokenizer.encode(poet_start, return_tensors='pt').to(model.device)

        # generate a continuation to it
        out = model.generate(
                tokenized_poet_start,
                max_new_tokens=256,
                do_sample=(not NOSAMPLE),
                # top_p=0.7,
                top_k=50,
                # no_repeat_ngram_size=2,
                pad_token_id= tokenizer.pad_token_id,
                temperature=temperature,
                tokenizer=tokenizer,
                eos_token_id = tokenizer.eos_token_id,
                **({'stop_strings': stop_strings} if stop_strings else {}),
        )

        if VERBOSE_INFO:
            logging.info(f"Tokenization in step {krok} with temperature {temperature}:")
            logging.info(_show_tokenization(tokenizer, out[0])) 

        # decode and return
        full = tokenizer.decode(out[0])
        generated = tokenizer.decode(out[0][len(tokenized_poet_start[0]):])

        return full, generated
    return g

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

def generuj_mc(model, tokenizer, template, params):

    gen = _generate(model, tokenizer, params.get('temperature'))

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

def generuj_tm(model, tokenizer, template, params_orig):

    params = params_orig.copy() # TODO fix this ugly hack

    gen = _generate(model, tokenizer, params.get('temperature'))

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
            rhyme_scheme_tm = " ".join(list(params['rhyme_scheme'].replace("X", "x")))
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
        for _ in range(verses_count):
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
                poem += f" {params['syllables_count']} #"
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

def generuj(model, tokenizer, template, params):
    logging.info(f'Generating with params: {params}')
    if params.get('modelspec') == 'tm':
        return generuj_tm(model, tokenizer, template, params)
    else:
        return generuj_mc(model, tokenizer, template, params)

def main_server(modelspec, port):
    # zmq mode
    logging.info(f'Starting zmq with {modelspec} model on port {port}')

    import zmq
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://*:{port}")
    model, tokenizer, template = load_models(modelspec)

    while True:
        params = json.loads(socket.recv())
        params['modelspec'] = modelspec
        result = json.dumps(generuj(model, tokenizer, template, params))
        socket.send_string(result)

def main_standalone(modelname, repeat=False, repeat_n=1, json_file=None, clean_output=False):
    # direct mode
    model, tokenizer, template = load_models(modelname)
    if json_file:
        with open(json_file, 'r') as f:
            params = json.load(f)
    else:
        params = {
            'modelspec': modelname,
            'temperature': 1,
            'rhyme_scheme': '',
            #'first_words': ['První', 'Druhá', 'Třetí', 'Čtvrtá'],
            'first_words': [],
            'verses_count': 0,
            'syllables_count': 0,
            'metre': '',
            'max_strophes': 2,
            'anaphors': [],
            'epanastrophes': [],
            }
    i = 0
    while True:
        result, clean_res, _, _ = generuj(model, tokenizer, template, params)
        if clean_output:
            if clean_output == 'json':
                print(json.dumps('\n'.join(clean_res), ensure_ascii=False))
            else:
                print('<|begin|>')
                print('\n'.join(clean_res))
        else:
            print(result)
        i += 1
        logging.info(f"Generated {i} poem" + "s" * (i > 1))
        if repeat:
            continue
        if repeat_n <= 1:
            break
        repeat_n -= 1

def parse_args():
    global MODEL_TM, VERBOSE_INFO, LOAD16BIT, NOSAMPLE
    argparser = argparse.ArgumentParser(description='Generate poetry with LLMs')
    argparser.add_argument('model', type=str, help='Model to use')
    argparser.add_argument('port', type=int, nargs='?', help='Port to use')
    argparser.add_argument('--verbose', action='store_true', help='Verbose output')
    argparser.add_argument('--repeat', action='store_true', help='Repeat forever')
    argparser.add_argument('--repeat_n', type=int, help='Repeat N times')
    argparser.add_argument('--16bit', action='store_true', help='Use 16bit model')
    argparser.add_argument('--greedy', action='store_true', help='Use greedy decoding')
    argparser.add_argument('--json', type=str, help='JSON file to use')
    argparser.add_argument('--clean', action='store_true', help='Clean output')
    argparser.add_argument('--clean_json', action='store_true', help='Clean JSON output')
    argparser.add_argument('--checkpoint', type=str, help='Checkpoint to use')
    args = argparser.parse_args()

    assert args.model in ['mc', 'tm']

    if args.checkpoint:
        MODEL_TM = args.checkpoint

    if args.verbose:
        VERBOSE_INFO = True

    if vars(args).get('16bit', False):
        LOAD16BIT = True
        logging.info("Loading in 16bit.")

    if args.greedy:
        NOSAMPLE = True
    
    return args

if __name__=="__main__":
    args = parse_args()
    if args.port:
        main_server(args.model, args.port)
    else:
        main_standalone(args.model,
                        repeat=args.repeat,
                        **({'repeat_n': args.repeat_n} if args.repeat_n else {}),
                        json_file=args.json,
                        clean_output='json' if args.clean_json else args.clean,
                        )
