#!/usr/bin/env python3
#coding: utf-8
"""Poem analysis (kveta + measures) as a ZMQ REP worker, the same way gen.py
serves the generator models.

    python3 analyze.py [port]        # default: $ANALYZE_PORT or 5013

Protocol: one JSON object in, one JSON object out (see analyze_poem).
"""

import json
import logging
import os
import sys
import traceback

sys.path.append("../kveta")
sys.path.append("../scripts/diphthongs")
from kveta import okvetuj, okvetuj_ccv
from get_measures import get_measures_from_analyzed_poem, get_measures_fast

logging.basicConfig(
    format='%(levelname)s %(asctime)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO)

DEFAULT_PORT = int(os.getenv('ANALYZE_PORT', 5013))


def analyze_poem(request):
    """Analyze one poem. Pure function of its argument, JSON-serialisable in
    and out, so the same code can be called directly or through ZMQ.

    request keys:
      id            optional, echoed back unchanged
      text          plain text (stanzas separated by blank lines)  -- OR --
      body          CCV verse list already in the DB (okvetuj_ccv path)
      measures      bool, default True: compute measures (text input only)
      fast          bool, default False: get_measures_fast only, no kveta
      meaning       bool, default False: make the LLM meaning call inside
                    the worker (otherwise the caller adds 'chatgpt_meaning')
      rhyme_scheme  optional hint for rhyme_scheme_accuracy
      metre         optional hint ('T','J','D','A') for metre_accuracy

    reply keys:
      id            as in the request
      body          analyzed verse list (not with fast=True)
      metres        overall metre probabilities (text input, full path only)
      measures      measures dict (if requested)
      error         traceback string; on error no other result keys are set
    """
    reply = {}
    if 'id' in request:
        reply['id'] = request['id']
    try:
        text = request.get('text')
        body = request.get('body')
        if (text is None) == (body is None):
            raise ValueError("exactly one of 'text' or 'body' must be given")
        want_measures = request.get('measures', True)
        fast = request.get('fast', False)
        parameters = {'meaning': request.get('meaning', False)}
        for key in ('rhyme_scheme', 'metre'):
            if request.get(key):
                parameters[key] = request[key]

        if body is not None:
            # stored KCV poem: light pass, measures are known not to work here
            reply['body'] = okvetuj_ccv(body)
        elif fast:
            if want_measures:
                reply['measures'] = get_measures_fast(text, parameters)
        else:
            output, _k = okvetuj(text)
            reply['body'] = output[0]['body']
            reply['metres'] = output[0]['metres']
            if want_measures:
                reply['measures'] = get_measures_from_analyzed_poem(
                        reply['body'], parameters)
    except Exception:
        logging.exception("analyze_poem failed")
        reply = {'error': traceback.format_exc()}
        if 'id' in request:
            reply['id'] = request['id']
    return reply


def main_server(port):
    import zmq
    logging.info('Starting zmq analysis worker on port %s', port)
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://*:{port}")
    while True:
        try:
            request = json.loads(socket.recv())
        except Exception:
            logging.exception("bad request")
            socket.send_string(json.dumps({'error': traceback.format_exc()}))
            continue
        socket.send_string(json.dumps(analyze_poem(request)))


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PORT
    main_server(port)
