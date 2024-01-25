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
thread = client.beta.threads.create()

MESSAGE = "Napište báseň o přírodě ve městě."

def talk(message=MESSAGE):
    # add message to thread
    msg = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=message
    )

    # run the assistant
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )

    # wait for answer
    while not run.status == "completed":
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )

    # extract response text
    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )
    text = messages.data[0].content[0].text.value
    
    return text

print(MESSAGE)
print(talk())
while True:
    message = input()
    print(talk(message))



