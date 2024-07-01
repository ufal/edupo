import sqlite3
import json

sqlite3.register_converter("json", json.loads)

diphthongs_dict = {'ou': '0', 'au': '1',  'eu': '2'}

with sqlite3.connect("../new.db", detect_types=sqlite3.PARSE_DECLTYPES) as db:
    poems = db.execute("SELECT body FROM poems;").fetchall()

words = ((word['token_lc'], word['phoebe']) for poem in poems for stanza in poem[0] for verse in stanza for word in verse['words'])

for a, b in words:
    for d in diphthongs_dict.keys():
        if d in a:
            print(f"{a},{b}")
            break