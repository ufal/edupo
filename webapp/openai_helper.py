#!/usr/bin/env python

import sys
from openai import OpenAI

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


if __name__=="__main__":
    prompt = input("Zadej prompt: ")
    print(generate_with_openai_simple(prompt))

