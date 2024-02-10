#!/usr/bin/env python3
#coding: utf-8

import sys
import requests
import io
import base64
import os
import os.path
import unidecode
import re
from PIL import Image, PngImagePlugin
import json
import logging
import random
from openai import OpenAI

### Image generation

HASH_WIDTH_BYTES = sys.hash_info.width//8

SDURL = 'http://ufallab.ms.mff.cuni.cz:8457'

SDURL_TXT2IMG = f'{SDURL}/sdapi/v1/txt2img'

# Directory with generated images
IMGDIR = 'genimgs'

# Adapted from THEaiTRE server
def text2id(text, add_text=False):
    # hash
    # ! seed is not stable, must run python with PYTHONHASHSEED=0
    hash_bytes = hash(text).to_bytes(HASH_WIDTH_BYTES, 'big', signed=True)
    hash64 = base64.urlsafe_b64encode(hash_bytes).decode('ascii')

    if add_text:
        text = unidecode.unidecode(text)
        text = re.sub(r'[-–— ]', '_', text)
        text = re.sub(r'[^a-zA-Z0-9_]', '', text)
        if len(text) > 64:
            text = text[:32] + '-' + text[-32:]
        return hash64 + text
    else:
        return hash64

def store_image(imgdata, filename):
    bytestream = io.BytesIO(base64.b64decode(imgdata))
    
    with open(filename, "wb") as outfile:
        outfile.write(bytestream.getbuffer())

# Based on https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/API
def generate_image_sd(prompt, seed, filename):
    payload = {
        "prompt": prompt,
        "steps": 13,
        "cfg_scale": 10,
        "seed": seed
    }

    response = requests.post(SDURL_TXT2IMG, json=payload)

    imgdata = response.json()['images'][0].split(",",1)[0]
    store_image(imgdata, filename)


# https://platform.openai.com/docs/guides/images/usage?context=python
# https://platform.openai.com/docs/api-reference/images/create
def generate_image_openai(prompt, filename):
    with open('apikey.txt') as infile:
        apikey = infile.read().strip()
    
    client = OpenAI(
        organization='org-926n4JNQeMTeU94X6FKZS8c3',
        api_key=apikey
    )
    
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
        response_format="b64_json",
    )

    # response.data[0].revised_prompt

    imgdata = response.data[0].b64_json
    store_image(imgdata, filename)

def generate_image(prompt, seed, filename):
    try:
        generate_image_openai(prompt, filename)
    except:
        generate_image_sd(prompt, seed, filename)


def _get_image_for_line(line, seed):
    try:
        filename = text2id(line) + '_' + str(seed)
        filename_full = f'{IMGDIR}/{filename}.png'
        if not os.path.isfile(filename_full):
            generate_image(line, seed, filename_full)
    except Exception as e:
        message = f'AI Soul: Cannot generate image "{filename}" for "{line}": {e}'
        logging.warning(message)
        print(message)
        filename = "DEFAULTIMAGE"
    
    return filename

def get_image_for_line(line, seed = None):
    if not seed:
        seed = random.randint(0, 10000000)
    filename = _get_image_for_line(line, seed)
    return filename

if __name__=="__main__":
    line = input('Image decsription:')
    print(f"{IMGDIR}/{get_image_for_line(line, 1987)}.png")
    
