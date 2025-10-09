#!/usr/bin/env python

from openai import OpenAI
import base64
import io

import logging
logging.basicConfig(
    format='%(levelname)s %(asctime)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO)

# OpenAI key
KEY_PATH = '/net/projects/EduPo/data/apikey.txt'

# OpenRouter key
OR_KEY_PATH = '/net/projects/EduPo/data/apikey_or.txt'

def generate_with_openai(messages, model="gpt-4o-mini", max_tokens=500, temperature=0):
    # OPENAI or OPENROUTER?
    # OPENROUTER model name always has '/' in it
    use_or = '/' in model

    # OPENAI SETUP
    # path to file with authentication key
    key_path = OR_KEY_PATH if use_or else KEY_PATH
    with open(key_path) as infile:
        apikey = infile.read().rstrip()
    try:
        if use_or:
            client = OpenAI(api_key=apikey, base_url="https://openrouter.ai/api/v1")
        else:
            client = OpenAI(api_key=apikey)
    except:
        logging.exception("EXCEPTION Neúspěšná inicializace OpenAI.")

    # https://platform.openai.com/docs/guides/chat/introduction
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=1,
            stop=[],  # can be e.g. stop = ['\n']
            presence_penalty=0,
            frequency_penalty=0,
            logit_bias={},
            extra_headers={ "X-Title": "EduPo" },
        )
        logging.debug(response)
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

from collections import defaultdict
def generate_poem_with_openai(params, model="gpt-4o-mini"):
    # set all unknown to ''
    params = defaultdict(str, params)

    REASONING = 'gpt-5' in model

    if REASONING:
        plan = "Begin with a concise checklist (3-7 bullets) of what you will do; keep items conceptual, not implementation-level.\n"
        validation = "After generating the poem, validate in 1-2 lines that all output requirements are met (correct header, stanza and line formatting, no extra content), and proceed or self-correct if not.\n"
    else:
        plan = ""
        validation = ""

    system=f"""You are a renowned 19th-century Czech poet, an expert in the Czech language known for your mastery of rich, poetic, and archaic vocabulary. Unless otherwise instructed, compose rhymed poetry in a standard poetic metre such as trochee, iamb, or dactyl. Your poetry should evoke deep emotions and subtle feelings. Poems should be of medium length—typically 4 to 20 verses unless specified. Each verse should be on its own line, and stanzas must be separated by exactly one blank line.

{plan}
When generating output, strictly follow this sequence:
- The first line must be formatted as 'Author Name: Poem Title'.
- If both author and title are provided, use them exactly as given.
- If only an author or only a title is provided, use the specified name and invent the missing detail.
- If neither is provided, invent both the author and the title.

Continue with the poem text, one verse per line, and insert a single blank line between stanzas, accurately preserving stanza structure.

{validation}
Output must contain only the author name, poem title, and poem text. Do not include any additional commentary or formatting.

## Output Format
Strictly use this structure:

Author Name: Poem Title
Verse 1
Verse 2

(stanza break: blank line)
Verse 3
Verse 4

... etc.

If a title and/or author is specified, use them exactly as given, inventing any missing part as needed. 
Between stanzas, use exactly one blank line. 
Do not output any other content or formatting."""

    prompt_parts = list()
    prompt_parts.append('Napiš českou báseň.')
    if params['rhyme_scheme']:
        prompt_parts.append(f"Použij rýmové schéma {params['rhyme_scheme']}.")
    if params['verses_count']:
        prompt_parts.append(f"Každá sloka by měla mít {params['verses_count']} veršů.")
    if params['syllables_count']:
        prompt_parts.append(f"První verš by měl mít {params['syllables_count']} slabik.")
    if params['metre']:
        prompt_parts.append(f"Metrum básně by mělo být {params['metre']}.")
    if params['first_words'] and any(params['first_words']):
        prompt_parts.append(f"První slova veršů by postupně měla být následující: {';'.join(params['first_words'])}.")
    if params['max_strophes']:
        if params['max_strophes'] == 1:
            slok = 'sloku'
        elif params['max_strophes'] < 5:
            slok = 'sloky'
        else:
            slok = 'slok'
        prompt_parts.append(f"Báseň by měla mít maximálně {params['max_strophes']} {slok}.")
    if params['form']:
        prompt_parts.append(f"Pevná forma básně by měla být {params['form']}.")
    if params['author_name'] and params['author_name'] != 'Anonym':
        prompt_parts.append(f"Báseň by měla být ve stylu známého českého autora, který se jmenoval {params['author_name']}.")
    if params['title'] and params['title'] != 'Bez názvu':
        prompt_parts.append(f"Název básně je: {params['title']}.")
    # TODO anaphors, epanastrophes
    prompt = ' '.join(prompt_parts)
    logging.info('TEXTGEN Prompt: ' + show_short(prompt))
    
    max_tokens = 500
    if params['verses_count'] or params['max_strophes']:
        verses = params['verses_count'] if params['verses_count'] else 4
        strophes = params['max_strophes'] if params['max_strophes'] else 4
        # max 50 per verse + title + author name
        max_tokens = 50 * verses * strophes + 100
    if 'gpt-5' in model:
        # reasoning models: add reasoning tokens
        max_tokens += 4000
    logging.info(f'TEXTGEN max_tokens: {max_tokens}')

    messages=[
        {"role": "system", "content": system},
        {"role": "user", "content": prompt},
    ]
    
    # TODO default teď máme 1, chceme to tak i pro GPT?
    if params['temperature']:
        temperature = params['temperature']
    else:
        temperature = 0.5

    output = generate_with_openai(messages, model, max_tokens, temperature)
    
    lines = output.split('\n')
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
    
    raw_output = f"System prompt: {system}\n\nUser prompt: {prompt}\n\nGenerated output:\n\n{output}"

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
    GEN_POEM = False
    GEN_TEXT = True
    GEN_IMG = False

    if GEN_POEM:
        title = input("Zadej název básně: ")
        author_name = input("Zadej jméno autora: ")
        
        for model in [
            "openai/gpt-4o-mini",
            "openai/gpt-5-mini",
            "anthropic/claude-sonnet-4.5",
            "google/gemini-2.5-flash",
            ]:
            print(f"USING OPENROUTER {model}")
            _, text, _, _ = generate_poem_with_openai(
                    params={'title': title, 'author_name': author_name},
                    model=model)
            print(*text, sep="\n")
    
    if GEN_TEXT:
        prompt = input("Zadej prompt: ")
        
        model="gpt-4o-mini"
        print(f"USING OPENAI {model}")
        print(generate_with_openai_simple(prompt, model=model))

        for model in [
            "openai/gpt-4o-mini",
            "openai/gpt-5-mini",
            # "anthropic/claude-sonnet-4.5",
            # "google/gemini-2.5-flash",
            ]:
            print(f"USING OPENROUTER {model}")
            print(generate_with_openai_simple(prompt, model=model, max_tokens=5000))

    if GEN_IMG:
        IMGFILE='image.png'
        image_desc = generate_image_with_openai(prompt, IMGFILE)
        print(f'Obrázek: {IMGFILE}. ({image_desc})')

