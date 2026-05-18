import json
from contextlib import redirect_stdout
import sys
import tqdm
with redirect_stdout(sys.stderr):
    import unsloth
    import gen

gen.LOAD16BIT = True

sys.path.append("../kveta")
sys.path.append("../scripts/diphthongs")
import kveta

import argparse

parse = argparse.ArgumentParser(description='Generování básní s použitím modelu.')
parse.add_argument('--model', type=str, default='tm')
parse.add_argument('--rhyme', type=str, default='AABB', help='Schéma rýmu (např. AABB, ABAB)')
parse.add_argument('--id', type=int, default=None, help='ID básně (pro replikaci)')

args = parse.parse_args()


problem_words = ['žid', 'černý', 'šuk', 'kokot', '– – –', 'orgie', 'hovno', 'blb', 'chám', 'krv', 'krev']

def poem_ok(poem, scheme):
    verse = poem['verse']
    if len(verse) != 9: return False
    for i in [0,1,2,3,5,6,7,8]:
        if len(verse[i]) == 0: return False
    if len(verse[4]) != 0: return False
    txt = "\n".join(verse).lower()
    for w in problem_words:
        if w in txt: return False
    if "komunista" in txt: print(txt)
    okv = kveta.okvetuj(txt)
    rhymes = [l['rhyme'] for l in okv[0][0]['body']]
    if scheme == 'AABB':
        if rhymes[0] != rhymes[1]: return False
        if rhymes[2] != rhymes[3]: return False
        if rhymes[4] != rhymes[5]: return False
        if rhymes[6] != rhymes[7]: return False
    elif scheme == 'ABAB':
        if rhymes[0] != rhymes[2]: return False
        if rhymes[1] != rhymes[3]: return False
        if rhymes[4] != rhymes[6]: return False
        if rhymes[5] != rhymes[7]: return False
    return True

SLOVA = [
    [
        "Jahoda", "Jablko", "Banán", "Pomeranč", "Borůvka", "Švestka"
    ],
    [
        "Špičatá", "Zvířecí", "Kouzelná", "Královská", "Nadýchaná", "Mimozemská"
    ],
    [
        "Radost", "Klid", "Zloba", "Spokojenost", "Zmatek", "Překvapení"
    ],
    [
        "Boty", "Tlapy", "Duch", "Noblesa", "Drápy", "Chapadla"
    ]
]

with redirect_stdout(sys.stderr):
    model, tokenizer, template = gen.load_models(args.model)

params = {
            'modelspec': args.model,
            'temperature': 1,
            'rhyme_scheme': args.rhyme,
            'first_words': ['První', 'Druhá', 'Třetí', 'Čtvrtá'],
            'verses_count': 0,
            'syllables_count': 8,
            'metre': '',
            'max_strophes': 2,
            'anaphors': [],
            'epanastrophes': [],
            }

total_poems = len(SLOVA[0]) * len(SLOVA[1]) * len(SLOVA[2]) * len(SLOVA[3])
if args.id is not None:
    total_poems = 1
pbar = tqdm.tqdm(total=total_poems, desc="Generating poems")
for i1, w1 in enumerate(SLOVA[0]):
    for i2, w2 in enumerate(SLOVA[1]):
        for i3, w3 in enumerate(SLOVA[2]):
            for i4, w4 in enumerate(SLOVA[3]):
                o_id = i1 * (6 ** 3) + i2 * (6 ** 2) + i3 * 6 + i4
                if args.id is not None and args.id != o_id:
                    continue
                op = 0
                while True:
                    prvni_slova = [w1, w2, w3, w4]
                    params['first_words'] = [w for w in prvni_slova]
                    result, clean_res, _, _ = gen.generuj(model, tokenizer, template, params)
                    out = {}
                    out['id'] = o_id
                    out['slova'] = prvni_slova
                    out['verse'] = clean_res
                    if poem_ok(out, args.rhyme):
                        break
                    else:
                        op += 1
                        if op > 50:
                            out = {}
                            break
                        continue
                print(json.dumps(out, ensure_ascii=False))
                pbar.update(1)
pbar.close()
