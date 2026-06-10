#!/usr/bin/env python3
# coding: utf-8
"""Generate a /hodnoceni evaluation set with the latest finetuned Format-V4 model.

Produces a JSONL file (one poem per line, in the Format V4 JSON structure that
``scripts/finetuning/format_v4.py`` emits) ready to drop into
``backend/hodnoceni_data/``.

By default it generates three poems:
  1. in the style of Karel Hynek Mácha
  2. in the style of František Gellner
  3. with no author

The model is the latest finetuned V4 checkpoint under
``/lnet/ms/projects/EduPo/tomas/outputs/dynamic_json/`` (auto-detected).

Usage (needs the ``edupo`` conda env and a GPU):
    python gen_eval_set.py
    python gen_eval_set.py --out hodnoceni_data/my_set.jsonl --temperature 0.8
    python gen_eval_set.py --checkpoint /path/to/checkpoint-XXXX
"""

import argparse
import json
import os
import re
import sys

# Latest finetuned V4 (Format V4 JSON) training run.
DEFAULT_MODEL_DIR = '/lnet/ms/projects/EduPo/tomas/outputs/dynamic_json'

# Authors to condition on, in the canonical "Surname, Name" form used in the
# training data (see backend/authors). None == no author (omit the field).
DEFAULT_SPECS = [
    {'author': 'Mácha, Karel Hynek'},
    {'author': 'Gellner, František'},
    {'author': None},
]


def find_latest_checkpoint(model_dir):
    """Return the checkpoint dir with the highest step number under model_dir."""
    checkpoints = []
    for name in os.listdir(model_dir):
        m = re.fullmatch(r'checkpoint-(\d+)', name)
        if m and os.path.isdir(os.path.join(model_dir, name)):
            checkpoints.append((int(m.group(1)), name))
    if not checkpoints:
        raise FileNotFoundError(f'No checkpoint-* dirs found in {model_dir}')
    _, name = max(checkpoints)
    return os.path.join(model_dir, name)


def build_prompt(author=None, stanzas_count=3, predict_title=True):
    """Build the Format V4 JSON prefix up to (and including) the open stanzas list.

    Mirrors the prefix produced by FormatV4.format_poem (format_v4.py): the
    leading format keys, then metadata (order is irrelevant — it is shuffled in
    training), then verse_regenerate / stanzas_count, then the open "stanzas".
    We fix the *_format choices to "before" so each generated verse carries its
    metre, syllable count and rhyme info (which the /hodnoceni page displays).

    With predict_title=True we put ``"title": null`` in the prefix — this is the
    TitleFormat.PREDICT mode: the model writes the poem first and then guesses
    the title *after* the stanzas as a ``"title_answer"`` footer entry.
    """
    parts = [
        '"format": "v4"',
        '"syllables_format": "before"',
        '"metre_format": "before"',
        '"rhyme_format": "before"',
        '"rhyme_schemes": true',
    ]
    if author:
        parts.append(f'"author": {json.dumps(author, ensure_ascii=False)}')
    if predict_title:
        parts.append('"title": null')
    parts.append('"verse_regenerate": false')
    parts.append(f'"stanzas_count": {stanzas_count}')
    return '{' + ', '.join(parts) + ',\n"stanzas": [\n'


def extract_first_json_object(text):
    """Extract the first complete top-level JSON object from text.

    The model output is the prompt prefix followed by the generated stanzas and
    closing braces (and possibly an EOS marker / trailing junk). We scan brace
    depth, ignoring braces inside strings, and return the substring of the first
    balanced {...}. Returns None if no balanced object is found.
    """
    start = text.find('{')
    if start == -1:
        return None
    depth = 0
    in_string = False
    escape = False
    for i in range(start, len(text)):
        ch = text[i]
        if in_string:
            if escape:
                escape = False
            elif ch == '\\':
                escape = True
            elif ch == '"':
                in_string = False
        else:
            if ch == '"':
                in_string = True
            elif ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    return text[start:i + 1]
    return None


def make_generate_fn(model, tokenizer, temperature, max_new_tokens):
    """Return g(prompt) -> full decoded text (prompt + continuation)."""
    def g(prompt):
        prompt = prompt.replace('<|begin_of_text|>', '')
        tokenized = tokenizer.encode(prompt, return_tensors='pt').to(model.device)
        out = model.generate(
            tokenized,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            top_k=50,
            temperature=temperature,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id,
            tokenizer=tokenizer,
        )
        return tokenizer.decode(out[0])
    return g


def clean_decoded(text):
    """Strip special tokens from a decoded sequence."""
    for tok in ('<|begin_of_text|>', '<|end_of_text|>', '<|eot_id|>'):
        text = text.replace(tok, '')
    return text


def generate_poem(generate, author, stanzas_count, predict_title=True, attempts=3):
    """Generate one poem dict for the given author, retrying on parse failure."""
    prompt = build_prompt(author=author, stanzas_count=stanzas_count,
                          predict_title=predict_title)
    for attempt in range(1, attempts + 1):
        decoded = clean_decoded(generate(prompt))
        candidate = extract_first_json_object(decoded)
        if candidate is not None:
            try:
                poem = json.loads(candidate)
            except json.JSONDecodeError as e:
                print(f'    attempt {attempt}: JSON decode failed ({e}), retrying',
                      file=sys.stderr)
                continue
            if poem.get('stanzas') and any(
                    st.get('verses') for st in poem['stanzas']):
                return poem
            print(f'    attempt {attempt}: empty stanzas, retrying', file=sys.stderr)
        else:
            print(f'    attempt {attempt}: no balanced JSON object, retrying',
                  file=sys.stderr)
    raise RuntimeError(f'Failed to generate a valid poem for author={author!r} '
                       f'after {attempts} attempts')


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--checkpoint', default=None,
                    help='Checkpoint dir (default: latest under %s)' % DEFAULT_MODEL_DIR)
    ap.add_argument('--out', default='hodnoceni_data/eval_set.jsonl',
                    help='Output JSONL path (default: %(default)s)')
    ap.add_argument('--temperature', type=float, default=0.8)
    ap.add_argument('--max-new-tokens', type=int, default=1024)
    ap.add_argument('--stanzas', type=int, default=3,
                    help='Number of stanzas to request per poem (default: %(default)s)')
    ap.add_argument('--no-title', action='store_true',
                    help='Do not ask the model to guess a title (default: guess title after the poem)')
    ap.add_argument('--seed', type=int, default=None,
                    help='Optional generation seed for reproducibility')
    args = ap.parse_args()

    checkpoint = args.checkpoint or find_latest_checkpoint(DEFAULT_MODEL_DIR)
    print(f'Loading model from {checkpoint} ...', file=sys.stderr)

    from unsloth import FastLanguageModel
    import torch
    if args.seed is not None:
        torch.manual_seed(args.seed)

    model, tokenizer = FastLanguageModel.from_pretrained(
        checkpoint,
        dtype=torch.bfloat16,
        load_in_4bit=False,
    )
    FastLanguageModel.for_inference(model)
    print('Model loaded.', file=sys.stderr)

    generate = make_generate_fn(model, tokenizer, args.temperature, args.max_new_tokens)

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, 'w', encoding='utf-8') as f:
        for spec in DEFAULT_SPECS:
            author = spec['author']
            label = author if author else '(no author)'
            print(f'Generating poem for {label} ...', file=sys.stderr)
            poem = generate_poem(generate, author, args.stanzas,
                                 predict_title=not args.no_title)
            # Normalise to a single JSONL line.
            f.write(json.dumps(poem, ensure_ascii=False) + '\n')
            n_verses = sum(len(st.get('verses', [])) for st in poem['stanzas'])
            print(f'  -> {len(poem["stanzas"])} stanzas, {n_verses} verses',
                  file=sys.stderr)

    print(f'Wrote {len(DEFAULT_SPECS)} poems to {args.out}', file=sys.stderr)


if __name__ == '__main__':
    main()
