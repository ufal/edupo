#!/usr/bin/env python3
#coding: utf-8

import sys

import logging
logging.basicConfig(
    format='%(asctime)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO)

from openai import OpenAI

client = OpenAI(
  organization='org-926n4JNQeMTeU94X6FKZS8c3',
)


# openai.OpenAIError: The api_key client option must be set either by passing api_key to the client or by setting the OPENAI_API_KEY environment variable


# Upload a file with an "assistants" purpose
#wfile = client.files.create(
#  wfile=open("znalosti_wolker.docx", "rb"),
#  purpose='assistants'
#)
#logging.info(wfile)
#logging.info(wfile.id)
#
#wfile_id = 'file-uPtA6klLK5pmrVAXtactwwcc'
#
#assistant = client.beta.assistants.create(
#    name="GenZ Wolker 2 assistant",
#    instructions="GenZ Wolker 2, a modern embodiment of Jiří Wolker, speaks in informal Czech, infused with the slang of today's youth. This GPT is skilled in Czech poetry, embracing a range of topics with a playful, youthful tone. It keeps responses concise and accessible, using shorter sentences and limiting them to one or two paragraphs. Crucially, GenZ Wolker 2 consistently refers to the uploaded knowledge about Jiří Wolker's life to ensure its responses align with what the real Jiří Wolker might say. The language is creative, metaphorical, and distinctly Czech, mirroring the authentic voice of a modern poet.",
#    tools=[{"type": "retrieval"}],
#    model="gpt-4-1106-preview",
#    file_ids=[wfile]
#)
#logging.info(assistant)
#logging.info(assistant.id)

assistant_id = 'asst_oEwl7wnhGDi5JDvAdE92GgWk'

thread = client.beta.threads.create()
logging.info(thread)
logging.info(thread.id)

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Napište báseň o přírodě ve městě."
)
logging.info(message)

run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant_id,
  instructions="Jsem GenZ Wolker 2, mladý Jiří Wolker v moderním světě, vždy odkazující na své znalosti."
)
logging.info(run)

while not run.status == "completed":
    print(run.status)
    run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )

messages = client.beta.threads.messages.list(
  thread_id=thread.id
)

print(messages)


