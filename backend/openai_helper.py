#!/usr/bin/env python

from openai import OpenAI
import base64
import io

import logging
logging.basicConfig(
    format='%(asctime)s %(message)s',
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
    except Exception as e:
        print(e)

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
        # print(response)
        return response.choices[0].message.content

    except:
        logging.exception("EXCEPTION Neúspěšné generování pomocí OpenAI.")
        return None

def generate_with_openai_simple(prompt, system="You are a helpful assistant.", model="gpt-4o-mini", max_tokens=500):
    print('TEXTGEN Prompt:', show_short(prompt))
    messages=[
        {"role": "system", "content": system},
        {"role": "user", "content": prompt},
    ]
    return generate_with_openai(messages, model, max_tokens)

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
    except Exception as e:
        print(e)
    
    print('IMGGEN Prompt:', show_short(prompt))
    sanitized_prompt = sanitize_prompt(prompt)
    print('IMGGEN Sanitized:', show_short(sanitized_prompt))

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

