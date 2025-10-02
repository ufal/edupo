#!/usr/bin/env python

from openai import OpenAI
import base64
import io

import logging
logging.basicConfig(
    format='%(levelname)s %(asctime)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO)

KEY_PATH = '/net/projects/EduPo/data/apikey.txt'

def generate_with_openai(messages, model="gpt-4o-mini", max_tokens=500):
    # OPENAI SETUP
    # path to file with authentication key
    with open(KEY_PATH) as infile:
        apikey = infile.read().rstrip()
    try:
        client = OpenAI(api_key=apikey)
    except:
        logging.exception("EXCEPTION Neúspěšná inicializace OpenAI.")

    # https://platform.openai.com/docs/guides/chat/introduction
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=0,
            top_p=1,
            stop=[],  # can be e.g. stop = ['\n']
            presence_penalty=0,
            frequency_penalty=0,
            logit_bias={},
        )
        return response.choices[0].message.content

    except:
        logging.exception("EXCEPTION Neúspěšné generování pomocí OpenAI.")
        return None

def generate_with_openai_simple(prompt, system="You are a helpful assistant.", model="gpt-4o-mini", max_tokens=500):
    logging.info('TEXTGEN Prompt: ' + show_short(prompt))
    messages=[
        {"role": "system", "content": system},
        {"role": "user", "content": prompt},
    ]
    return generate_with_openai(messages, model, max_tokens)

def generate_poem_with_openai(params, model="gpt-4o-mini", max_tokens=500):
    system="You are a well-known 19th century Czech poet. You are a master of Czech language, using a large variety of Czech words, including archaic and poetic words. Unless instructed otherwise, you write rhymed poetry following standard poetic metre, such as trochee, iamb or dactyl. Your poems are beautiful, touching on delicate feelings and emotions. Your poems are of medium length, typically between 4 and 20 verses (unless instructed otherwise). Write poems with one verse per line, with empty lines used to separate stanzas. Unless an author name and/or title is specified, invent also an author name and title. In any case, your first line should be in the format 'Author Name: Poem Title'. The following lines hsould contain the text of the poem. Write only the author name, poem title, and poem text."
    prompt_parts = list()
    prompt_parts.append('Napiš českou báseň.')
    prompt = ' '.join(prompt_parts)
    logging.info('TEXTGEN Prompt: ' + show_short(prompt))
    messages=[
        {"role": "system", "content": system},
        {"role": "user", "content": prompt},
    ]

    raw_output = generate_with_openai(messages, model, max_tokens)
    
    lines = raw_output.split('\n')
    if ':' in lines[0]:
        author_name, title = lines[0].split(':', 1)
    else:
        author_name = 'Gustav Petr Tichý'
        title = lines[0]
    
    start = 1
    while start < len(lines) and lines[start] == '':
        start += 1
    if start < len(lines):
        clean_verses = lines[start:]
    else:
        clean_verses = []
    
    return raw_output, clean_verses, author_name, title.strip()

def sanitize_prompt(prompt):
    return generate_with_openai_simple(f"Uprav prompt od uživatele pro generování obrázku tak, aby byl v souladu se všemi zásadami. Na výstup vydej pouze upravený prompt. Prompt: {prompt}")

def show_short(text, maxlen=100):
    if len(text) < maxlen:
        return repr(text)
    else:
        return repr(text[:maxlen-20] + '...' + text[-20:])

# https://platform.openai.com/docs/guides/images/usage?context=python
# https://platform.openai.com/docs/api-reference/images/create
def generate_image_with_openai(prompt, filename):
    with open(KEY_PATH) as infile:
        apikey = infile.read().rstrip()
    try:
        client = OpenAI(api_key=apikey)
    except:
        logging.exception("EXCEPTION Neúspěšná inicializace OpenAI.")
    
    logging.info('IMGGEN Prompt: ' + show_short(prompt))
    sanitized_prompt = sanitize_prompt(prompt)
    logging.info('IMGGEN Sanitized: ' + show_short(sanitized_prompt))

    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=sanitized_prompt,
            size="1024x1024",
            quality="standard",
            n=1,
            response_format="b64_json",
        )
    except:
        logging.exception("EXCEPTION Neúspěšné generování obrázku pomocí OpenAI.")
        return None

    imgdata = response.data[0].b64_json
    store_image(imgdata, filename)

    return response.data[0].revised_prompt

def store_image(imgdata, filename):
    bytestream = io.BytesIO(base64.b64decode(imgdata))
    
    with open(filename, "wb") as outfile:
        outfile.write(bytestream.getbuffer())

if __name__=="__main__":
    prompt = input("Zadej prompt: ")
    
    result = generate_with_openai_simple(prompt)
    print(result)
    
    IMGFILE='image.png'
    image_desc = generate_image_with_openai(prompt, IMGFILE)
    print(f'Obrázek: {IMGFILE}. ({image_desc})')

