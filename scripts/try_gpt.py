#!/usr/bin/env python3
#coding: utf-8

import openai
from openai import OpenAI

def generate_with_openai(messages, model="gpt-3.5-turbo", max_tokens=500):
    
    # OPENAI SETUP
    # path to file with authentication key
    with open('apikey.txt') as infile:
        apikey = infile.read()
    try:
        client = OpenAI(api_key=apikey)
    except Exception as e:
        print(e)

    # https://platform.openai.com/docs/guides/chat/introduction
    try:
        response = client.chat.completions.create(
            model = model,
            messages = messages,
            max_tokens = max_tokens,
            temperature = 1,
            top_p = 1,
            stop = [], # can be e.g. stop = ['\n']
            presence_penalty = 0,
            frequency_penalty = 0,
            logit_bias = {},
            )
        # print(response)
        return response.choices[0].message.content
    
    except Exception as e:
        etype, value, traceback = sys.exc_info()
        print("EXCEPTION", e, etype, value, traceback, sep="\n")
        return None

if __name__=="__main__":
    messages = [
        {"role": "system", "content": "You are a profficient author of poems."},
        {"role": "user", "content": "Napiš báseň o ptakopyskovi. Použij trochej a rýmové schéma AABB."},
        #{"role": "assistant", "content": "To byl jednou jeden ptakopysk,"},
        #{"role": "user", "content": "Ale on měl velmi malý pysk."},
    ]
    print(generate_with_openai(messages))

