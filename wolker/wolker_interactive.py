#!/usr/bin/env python3
#coding: utf-8

import sys

with open('apikey.txt') as infile:
    apikey = infile.read()

from openai import OpenAI
import time

client = OpenAI(
    organization='org-926n4JNQeMTeU94X6FKZS8c3',
    api_key=apikey
)
assistant_id = 'asst_oEwl7wnhGDi5JDvAdE92GgWk'

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

def talk_threaded(message="Napište báseň o přírodě ve městě.", thread_id=None):
    if not thread_id:
        thread = client.beta.threads.create()
        thread_id = thread.id
    
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
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )

    result, roles = get_thread_messages(thread_id)

    return result, roles, thread_id

if __name__=="__main__":
    while True:
        message = input()
        print(talk(message))

