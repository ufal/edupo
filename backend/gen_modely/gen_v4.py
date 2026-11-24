"""Generator for the Format V4 (JSON) models trained on the dynamic dataset.

See scripts/finetuning/format_v4.py for the training format. Every poem is a
JSON object: a header with format switches and metadata, a list of stanzas
(each with a rhyme scheme and a list of verses) and an optional footer with
predicted metadata (title_answer, author_answer, ...).

We always ask for the "before" variant of the per-verse annotations, i.e.
{"metre": "T", "syllables": 8, "rhyme_with": "áj", "text": "..."}, so that
metre, syllable count and first words can be forced verse by verse.
"""

import json
import logging
import re

import torch
from unsloth import FastLanguageModel

from gen_eval_set import clean_decoded, extract_first_json_object

MODEL = '/net/projects/EduPo/data/hrabe_v2_epoch6'

# app form name -> form name used in the training data (poems.schemes.form)
FORMS = {
    'sonet': 'Sonet',
}

ATTEMPTS = 3
DEFAULT_STANZAS = 2


def load_model(modelspec=None, load16bit=True, model_path=None):
    model_path = model_path or MODEL
    logging.info("Loading model %s %s", modelspec, model_path)

    kwargs = {}
    if load16bit:
        kwargs['dtype'] = torch.bfloat16
        kwargs['load_in_4bit'] = False
    else:
        kwargs['load_in_4bit'] = True
        logging.info("Loading in 4bit.")
    model, tokenizer = FastLanguageModel.from_pretrained(model_path, **kwargs)
    FastLanguageModel.for_inference(model)

    logging.info("Model loaded: %s", modelspec)
    return model, tokenizer, None


# ---------------------------------------------------------------- prompt

def _header(params, stanzas_count):
    """Format V4 prefix up to (and including) the open stanzas list."""
    parts = [
        '"format": "v4"',
        '"syllables_format": "before"',
        '"metre_format": "before"',
        '"rhyme_format": "before"',
        '"rhyme_schemes": true',
    ]
    # missing author / title -> null = the model predicts it after the poem
    parts.append(f'"author": {json.dumps(params.get("author_name") or None, ensure_ascii=False)}')
    parts.append(f'"title": {json.dumps(params.get("title") or None, ensure_ascii=False)}')
    if params.get('year'):
        parts.append(f'"year": {int(params["year"])}')
    motives = [m.strip() for m in params.get('motives') or [] if m.strip()]
    if motives:
        parts.append(f'"motives": {json.dumps(motives, ensure_ascii=False)}')
    if params.get('collection_style'):
        parts.append(f'"book_title": {json.dumps(params["collection_style"], ensure_ascii=False)}')
    form = FORMS.get(params.get('form') or '')
    if form:
        parts.append(f'"form": {json.dumps(form, ensure_ascii=False)}')
    parts.append('"verse_regenerate": false')
    if stanzas_count:
        parts.append(f'"stanzas_count": {stanzas_count}')
    return '{' + ', '.join(parts) + ',\n"stanzas": [\n'


def _stanza_scheme(rhyme_scheme, stanza_index):
    """App scheme ('ABBA CDDC EFG EFG', 'AABB', 'XXX') -> V4 scheme of one
    stanza, letters renumbered from A within the stanza ('A B B A')."""
    parts = rhyme_scheme.split()
    letters = parts[stanza_index % len(parts)]
    renum = {}
    out = []
    for ch in letters.upper():
        if ch == 'X':
            out.append('x')
        else:
            renum.setdefault(ch, 'ABCDEFGHIJKLMNOPQRSTUVWYZ'[len(renum) % 25])
            out.append(renum[ch])
    return out


def _nth(value, index):
    """Int or list param -> value for the given index (cycling a list)."""
    if isinstance(value, list):
        return value[index % len(value)] if value else 0
    return value or 0


def _is_constrained(params):
    return bool(params.get('rhyme_scheme') or params.get('metre')
                or params.get('syllables_count') or params.get('verses_count')
                or any(w.strip() for w in params.get('first_words') or []))


# ---------------------------------------------------------------- generation

def _free(gen, poem, stop, max_new):
    """Let the model continue `poem` up to (not including) `stop`."""
    _, generated = gen(poem, stop_strings=[stop], max_new=max_new)
    generated = clean_decoded(generated)
    idx = generated.find(stop)
    return generated[:idx] if idx >= 0 else generated


def _json_string_body(text):
    """Make generated verse text safe inside a JSON string literal (the model
    may emit an unescaped quote or a newline)."""
    try:
        json.loads(f'"{text}"')
        return text
    except json.JSONDecodeError:
        return json.dumps(text.replace('\\"', '"'), ensure_ascii=False)[1:-1]


def _generate_constrained(gen, params):
    """Build the JSON structure ourselves and let the model fill the free
    slots verse by verse (rhyme scheme, metre, syllables, first words forced
    where given)."""
    stanzas_count = params.get('max_strophes') or DEFAULT_STANZAS
    metre = params.get('metre') or ''
    first_words = [w.strip() for w in params.get('first_words') or []]
    poem = _header(params, stanzas_count)
    global_verse = 0

    for s in range(stanzas_count):
        if s > 0:
            poem += ',\n'
        verses_count = _nth(params.get('verses_count'), s)

        # rhyme scheme of the stanza
        if params.get('rhyme_scheme'):
            scheme = _stanza_scheme(params['rhyme_scheme'], s)
        else:
            generated = _free(gen, poem + '{"rhyme_scheme": ', '"verses":', 30)
            m = re.search(r'"([A-Za-z ]+)"', generated)
            scheme = m.group(1).split() if m else []
            if not scheme:
                scheme = ['x'] * (verses_count or 4)
        if verses_count:
            scheme = (scheme + ['x'] * verses_count)[:verses_count]
        poem += '{"rhyme_scheme": ' + json.dumps(' '.join(scheme)) + ', "verses": [\n'

        # verses
        for v, letter in enumerate(scheme):
            if v > 0:
                poem += ',\n'
            poem += '{"metre": '
            if metre:
                poem += f'"{metre}", '
            else:
                poem += _free(gen, poem, '"syllables":', 10)
            poem += '"syllables": '
            syllables = _nth(params.get('syllables_count'), v)
            if syllables:
                poem += f'{syllables}, '
            else:
                poem += _free(gen, poem, '"rhyme_with":', 10)
            poem += '"rhyme_with": '
            if letter == 'x' or letter not in scheme[:v]:
                poem += 'null, '
            else:
                poem += _free(gen, poem, '"text":', 20)
            poem += '"text": "'
            word = first_words[global_verse] if global_verse < len(first_words) else ''
            if word:
                poem += json.dumps(word, ensure_ascii=False)[1:-1] + ' '
            poem += _json_string_body(_free(gen, poem, '"}', 80))
            poem += '"}'
            global_verse += 1
        poem += '\n]}'

    poem += '\n]'
    # footer: predicted title/author, closing brace
    _, generated = gen(poem, stop_strings=['}'], max_new=200)
    generated = clean_decoded(generated)
    end = generated.find('}')
    poem += generated[:end + 1] if end >= 0 else '}'
    return poem


def _generate_free(gen, params):
    stanzas_count = params.get('max_strophes') or 0
    poem = _header(params, stanzas_count)
    _, generated = gen(poem, max_new=1500)
    return poem + clean_decoded(generated)


# ---------------------------------------------------------------- parsing

def _unescape(json_string_body):
    try:
        return json.loads(f'"{json_string_body}"')
    except json.JSONDecodeError:
        return json_string_body


def _parse(raw, params):
    """-> (verses with '' between stanzas, author, title); verses empty on failure."""
    author = params.get('author_name')
    title = params.get('title')
    verses = []
    poem = None
    candidate = extract_first_json_object(raw)
    if candidate is not None:
        try:
            poem = json.loads(candidate)
        except json.JSONDecodeError as e:
            logging.warning("V4 output is not valid JSON: %s", e)

    if poem is not None:
        for stanza in poem.get('stanzas') or []:
            texts = [str(v.get('text') or '').strip() for v in stanza.get('verses') or []
                     if isinstance(v, dict)]
            texts = [t for t in texts if t]
            if texts:
                if verses:
                    verses.append('')
                verses.extend(texts)
        author = author or poem.get('author_answer') or poem.get('author')
        title = title or poem.get('title_answer') or poem.get('title')
    else:
        # broken JSON: salvage the verse texts
        verses = [_unescape(t) for t in re.findall(r'"text": "((?:[^"\\]|\\.)*)"', raw)]
        m = re.search(r'"title_answer": "((?:[^"\\]|\\.)*)"', raw)
        title = title or (_unescape(m.group(1)) if m else None)
        m = re.search(r'"author_answer": "((?:[^"\\]|\\.)*)"', raw)
        author = author or (_unescape(m.group(1)) if m else None)

    return verses, str(author or 'Anonym'), str(title or 'Bez názvu')


def generuj(gen, _template, params):
    if params.get('anaphors') or params.get('epanastrophes'):
        logging.info("Anaphors/epanastrophes are not supported by the V4 model, ignoring.")
    constrained = _is_constrained(params)

    raw, verses, author, title = '', [], 'Anonym', 'Bez názvu'
    for attempt in range(1, ATTEMPTS + 1):
        raw = _generate_constrained(gen, params) if constrained else _generate_free(gen, params)
        verses, author, title = _parse(raw, params)
        if verses:
            break
        logging.warning("Attempt %d: no verses parsed, retrying", attempt)

    return raw, verses, author, title
