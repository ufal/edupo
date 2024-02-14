#!/usr/bin/env python3
#coding: utf-8

with open('apikey.txt') as infile:
    apikey = infile.read().strip()

from openai import OpenAI
import time
import multiprocessing

import logging
logging.basicConfig(
    format='%(asctime)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO)

MAXTIME=100
SLEEPTIME=10

client = OpenAI(
    api_key=apikey
)
ASSISTANT_ID = 'asst_kZPGslLLlaNpwKPj6HOmoCAH'

def get_thread_messages(thread_id):
    # extract response text
    messages = client.beta.threads.messages.list(
        thread_id=thread_id
    )

    result = []
    roles = []
    for part in messages.data:
        result.append(part.content[0].text.value)
        roles.append(part.role)
    
    result.reverse()
    roles.reverse()

    return result, roles

def talk(message="Napište báseň o přírodě ve městě."):
    result, _, _ = talk_threaded(message)
    return result[-1]

def _talk_threaded(d,
        message="Napište báseň o přírodě ve městě.",
        assistant_id=ASSISTANT_ID,
        thread_id=None):

    starttime = time.time()
    
    if not thread_id:
        thread = client.beta.threads.create()
        thread_id = thread.id
    d['thread_id'] = thread_id

    # add message to thread
    msg = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message
    )

    # run the assistant
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
    )

    # wait for answer
    while not run.status == "completed":
        time.sleep(SLEEPTIME)
        spenttime = time.time() - starttime 
        logging.info(f'Time spent waiting so far: {spenttime}')
        if spenttime > MAXTIME:
            raise Exception('Max time reached')
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )


def talk_threaded(message="Napište báseň o přírodě ve městě.",
        assistant_id=ASSISTANT_ID,
        thread_id=None):

    manager = multiprocessing.Manager()
    d = manager.dict()

    p = multiprocessing.Process(target=_talk_threaded,
            args=(d, message, assistant_id, thread_id))
    p.start()
    p.join(MAXTIME)
    if p.is_alive():
        p.terminate()
        raise Exception('Max time reached')
    else:
        thread_id = d['thread_id']
        result, roles = get_thread_messages(thread_id)

    return result, roles, thread_id

def talk_simple(prompt, system_message="Jsi básník Jiří Wolker."):
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt},
    ]
    
    # This is the limit of the model
    model_max_tokens = 2048

    # How many tokens to generate max
    max_tokens = 500

    # Model identifier
    model = "gpt-3.5-turbo"
    
    response = client.chat.completions.create(
        model = model,
        messages = messages,
        max_tokens = max_tokens,
        )
    result = response.choices[0].message.content
    
    return result


if __name__=="__main__":
    while True:
        message = input()
        print('SIMPLE:')
        print(talk_simple(message))
        print('FULL:')
        print(talk(message))

