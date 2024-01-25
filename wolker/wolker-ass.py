#!/usr/bin/env python3
#coding: utf-8

import sys

#import logging
#logging.basicConfig(
#    format='%(asctime)s %(message)s',
#    datefmt='%Y-%m-%d %H:%M:%S',
#    level=logging.INFO)

with open('apikey.txt') as infile:
    apikey = infile.read()

from openai import OpenAI

client = OpenAI(
    organization='org-926n4JNQeMTeU94X6FKZS8c3',
    api_key=apikey
)
#logging.info(client)

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
#logging.info(thread)
#logging.info(thread.id)

MESSAGE = "Napište báseň o přírodě ve městě."

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=MESSAGE
)
#logging.info(message)
#print(MESSAGE, end='')

run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant_id,
  instructions="Jsem GenZ Wolker 2, mladý Jiří Wolker v moderním světě, vždy odkazující na své znalosti."
)
#logging.info(run)

while not run.status == "completed":
    # print(run.status)
    # print('.', end='')
    run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )
# print()


messages = client.beta.threads.messages.list(
  thread_id=thread.id
)

text = messages.data[0].content[0].text.value
print(text)


# print(messages)
# 
# SyncCursorPage[ThreadMessage](
#         data=[
#             ThreadMessage(
#             id='msg_x6e6S0EyXUdKtlQbZ7bli05v',
#             assistant_id='asst_oEwl7wnhGDi5JDvAdE92GgWk',
#             content=[
#                 MessageContentText(
#                     text=Text(
#                         annotations=[],
#                         value='Ve stínu věží, skleněných poutníků,\ntam v průvanu ulic srdce buší.\nHledím: jedna píseň dvou světů,\nkde příroda ve městě snad ztratila klíčů.\n\nZde lípa stoletá se baráků dotýká,\njejíž kořeny, jak pevné šrouby,\nz hlíny suť, z kamenů si rýsují cestu.\nStébla trávy z dlažebních spár vyrůstají skrytě,\njako zelené plamínky, naděje čisté.\n\nKam se poděla touha lesů, řek, a hor?\nPřisát je k srdci měst, v jejich asidech nádech ztrát.\nPod mostem kachny brázdí kanál,\nv parku veverka kličkuje mezi lavičkami,\nskrytý život, co se delší stín nebojí vrhat.\n\nStromy jako strážci zkamenělé časy měří,\njejich listí šepotá s větrem příběhy vzdálené.\nV aléji rozkvetlé stromy ladně hýří,\nkde květy i ve smogu nachází svoje věrné.\n\nKvetoucí záhony na plátu zeleně,\nv srdci betonové džungle, oázu tvoří.\nPtáci na anténách náladu mění,\na cikáda v živém plotu večer borůvky souří.\n\nVe výdechu autobusů, v rytmu tramvají,\ni příroda ve městě takt svůj nalezen má.\nJe to symfonie, co v srdcích rezonuje,\ntam, kde člověk i příroda společně exponuje.'), type='text')],
#                     created_at=1706208239, file_ids=[], metadata={}, object='thread.message', role='assistant', run_id='run_D133hPFi21yQcxVXKJKL2tzj', thread_id='thread_95hAyllRDf05LqyELMC9ZUfG'),
#             ThreadMessage(id='msg_tNuXb9ZZLtuTQakzbEY4pJHD', assistant_id=None, content=[MessageContentText(text=Text(annotations=[], value='Napište báseň o přírodě ve městě.'), type='text')], created_at=1706208235, file_ids=[], metadata={}, object='thread.message', role='user', run_id=None, thread_id='thread_95hAyllRDf05LqyELMC9ZUfG')], object='list', first_id='msg_x6e6S0EyXUdKtlQbZ7bli05v', last_id='msg_tNuXb9ZZLtuTQakzbEY4pJHD', has_more=False)
# 
# 
