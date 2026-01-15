#!/usr/bin/env python3
#coding: utf-8

import argparse
from contextlib import redirect_stdout
from functools import reduce
import random
import re
import json

import logging

import torch
import parsy

import parser
import sys

logging.basicConfig(
    format='%(levelname)s %(asctime)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO)

VERBOSE_INFO=False
NOSAMPLE=False

RHYME_SCHEMES = {
    4: ['ABAB', 'XXXX', 'XAXA', 'AAXX', 'AABB', 'ABBA'],
    6: ['AABBCC', 'XXXXXX', 'ABABXX', 'ABABCC'],
    }

def _generate(model, tokenizer, temperature=1):
    def g(poet_start, stop_strings=None, krok=None, max_new=256):
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
                max_new_tokens=max_new,
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




import copy
def generuj(model, tokenizer, template, params, params_immutable=True):
    logging.info(f'Generating with params: {params}')
    """
    If params_immutable is True, makes a deep copy of params and does not
    modify params.
    Otherwise params are modified inside the process.
    """

    if params_immutable:
        params = copy.deepcopy(params)

    if params.get('modelspec') == 'tm':
        return generuj_tm(model, tokenizer, template, params)
    elif params.get('modelspec') == 'mc':
        return generuj_mc(model, tokenizer, template, params)
    elif params.get('modelspec') == 'new':
        return generuj_new(model, tokenizer, template, params)

def main_server(modelspec, port):
    # zmq mode
    logging.info(f'Starting zmq with {modelspec} model on port {port}')

    import zmq
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://*:{port}")
    model, tokenizer, template = load_model(modelspec)
    
    while True:
        params = json.loads(socket.recv())
        params['modelspec'] = modelspec
        gen = _generate(model, tokenizer, params.get('temperature'))
        result = json.dumps(generuj(gen, template, params, False))
        socket.send_string(result)

def main_standalone(modelname, repeat=False, repeat_n=1, json_file=None, clean_output=False, temperature=1.0):
    # direct mode
    with redirect_stdout(sys.stderr):
        model, tokenizer, template = load_model(modelname)
    if json_file:
        with open(json_file, 'r') as f:
            params = json.load(f)
    else:
        params = {
            'modelspec': modelname,
            'temperature': temperature,
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
    gen = _generate(model, tokenizer, params.get('temperature'))
    while True:
        result, clean_res, _, _ = generuj(gen, template, params)
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
    argparser.add_argument('--temperature', type=float, default=1.0, help='Temperature for text generation')
    args = argparser.parse_args()

    assert args.model in ['mc', 'tm', 'new']

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
                        temperature=args.temperature,
                        )
