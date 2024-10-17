#!/usr/bin/env python

import sys
from openai import OpenAI
import base64
import io

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

    except Exception as e:
        etype, value, traceback = sys.exc_info()
        print("EXCEPTION", e, etype, value, traceback, sep="\n")
        return None

def generate_with_openai_simple(prompt, system="You are a helpful assistant.", model="gpt-4o-mini", max_tokens=500):
    messages=[
        {"role": "system", "content": system},
        {"role": "user", "content": prompt},
    ]
    return generate_with_openai(messages, model, max_tokens)

def sanitize_prompt(prompt):
    #return f'Generate an image according the user specification: {prompt}.  Change the prompt so that it is aligned with all policies.'
    return f'Vygeneruj obrázek podle uživatelského promptu. Uprav prompt tak, aby byl v souladu se všemi zásadami. Prompt: {prompt}'

# https://platform.openai.com/docs/guides/images/usage?context=python
# https://platform.openai.com/docs/api-reference/images/create
def generate_image_with_openai(prompt, filename):
    with open(KEY_PATH) as infile:
        apikey = infile.read().rstrip()
    try:
        client = OpenAI(api_key=apikey)
    except Exception as e:
        print(e)
    
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=sanitize_prompt(prompt),
            size="1024x1024",
            quality="standard",
            n=1,
            response_format="b64_json",
        )
    except Exception as e:
        etype, value, traceback = sys.exc_info()
        print("EXCEPTION", e, etype, value, traceback, sep="\n")
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

