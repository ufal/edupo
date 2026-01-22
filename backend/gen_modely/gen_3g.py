import logging
import re

import torch

from unsloth import FastLanguageModel

MODEL = '/net/projects/EduPo/data/new_model_5520'


def parse_poem_xml(xml_text: str) -> tuple[list[str], str, str]:
    """Parse poem XML, handling partial/incomplete XML gracefully.

    Returns:
        tuple: (verses, author, title)
        - verses: list of verse strings with empty strings between stanzas
        - author: extracted author or 'Anonym'
        - title: extracted title or 'Bez názvu'
    """
    # Extract author (try with closing tag first, then without for partial XML)
    author_match = re.search(r'<author>(.+?)</author>', xml_text, re.DOTALL)
    if author_match:
        author = author_match.group(1).strip()
    else:
        # Partial XML - author tag may not be closed
        author_match = re.search(r'<author>([^<]+)', xml_text)
        author = author_match.group(1).strip() if author_match else 'Anonym'

    # Extract title (same approach)
    title_match = re.search(r'<title>(.+?)</title>', xml_text, re.DOTALL)
    if title_match:
        title = title_match.group(1).strip()
    else:
        title_match = re.search(r'<title>([^<]+)', xml_text)
        title = title_match.group(1).strip() if title_match else 'Bez názvu'

    # Extract <regenerated> contents from full XML (they appear after </stanzas>)
    regenerated_contents = re.findall(r'<regenerated>(.+?)</regenerated>', xml_text, flags=re.DOTALL)

    # Extract stanzas section
    stanzas_match = re.search(r'<stanzas[^>]*>(.*?)(?:</stanzas>|$)', xml_text, re.DOTALL)
    if not stanzas_match:
        return [], author, title

    stanzas_content = stanzas_match.group(1)

    # Remove <motives>...</motives> blocks (can appear in header or footer)
    stanzas_content = re.sub(r'<motives>.*?</motives>', '', stanzas_content, flags=re.DOTALL)

    # Handle <regenerate/> markers: replace with content from corresponding <regenerated> tags
    regenerated_iter = iter(regenerated_contents)

    def replace_regenerate(match):
        try:
            return next(regenerated_iter)
        except StopIteration:
            return ''

    stanzas_content = re.sub(r'<regenerate/>', replace_regenerate, stanzas_content)

    # Split by <new_stanza/> markers
    stanza_parts = re.split(r'<new_stanza\s*/>', stanzas_content)

    verses = []
    for i, stanza in enumerate(stanza_parts):
        if i > 0 and verses:
            # Add empty line between stanzas (but not before first stanza)
            verses.append('')

        # Process each line in the stanza
        lines = stanza.strip().split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Skip metadata tags like <rhyme_scheme>, <motive>, <regenerated>
            if line.startswith('<rhyme_scheme') or line.startswith('<motive') or line.startswith('<regenerated'):
                continue

            # Extract verse text after inline metadata tags
            # Pattern: <metre>X</metre><syllables>N</syllables><rhyme_with>X</rhyme_with>TEXT
            verse_match = re.search(
                r'<metre>.*?</metre>\s*<syllables>.*?</syllables>\s*<rhyme_with>.*?</rhyme_with>\s*(.+)$',
                line
            )
            if verse_match:
                verse_text = verse_match.group(1).strip()
                if verse_text:
                    verses.append(verse_text)
            elif not line.startswith('<'):
                # Plain text line (no metadata tags)
                verses.append(line)

    return verses, author, title


def load_model(modelspec=None, load16bit=True, model_path=MODEL):

    logging.info(f"Loading model {modelspec} {model_path}")

    kwargs = {}
    if load16bit:
        kwargs['dtype'] = torch.bfloat16
        kwargs['load_in_4bit'] = False
    else:
        kwargs['load_in_4bit'] = True
        logging.info("Loading in 4bit.")
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_path,
        **kwargs,
        )
    FastLanguageModel.for_inference(model)

    #logging.info(f"model_3g: {model_path}")
    #logging.info(f"tokenizer_3g: {tokenizer}")

    logging.info("Model loaded: " + modelspec)
    return model, tokenizer, None

def generuj(gen, _, params):

    poem = '<poem>\n<format-v-3/>\n'
    if params.get('author_name', None):
        poem += f"<author>{params['author_name']}</author>\n"
    if params.get('title', None):
        poem += f"<title>{params['title']}</title>\n"
    if params.get('form', None):
        poem += f"<form>{params['form']}</form>\n"
    if params.get('motives', None):
        motives = [m.strip() for m in params['motives'] if m.strip()]
        if motives:
            poem += '<motives>\n'
            for motive in motives:
                poem += motive + "\n"
            poem += '</motives>\n'
    if params.get('max_strophes', 0) > 0:
        poem += f'<stanzas length="{params['max_strophes']}">\n'
    else:
        poem += '<stanzas>\n'
    
    _, generated = gen(poem, max_new=2048)

    poem += generated

    verses, author, title = parse_poem_xml(poem)

    return poem, verses, author, title
