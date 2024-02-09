#!/usr/bin/env python3
#coding: utf-8

import sys
import cgi
from wolker_interactive import talk


print("Content-type: text/html")
print()

form = cgi.FieldStorage()
topic = form.getvalue("topic",
    form.getvalue("topic_freeform", None))
content = form.getvalue("content", None)
verse1 = form.getvalue("verse1", '')
verse2 = form.getvalue("verse2", '')

options = [
        "slunce",
        "globální oteplování",
        "současná politická situace v Česku",
        "hromadění bohatsví",
        "válečná situace ve světě",
        ]

print(f"""
<!DOCTYPE html>
    <html lang="cs">
    <head>
        <title>Společné psaní básně s Wolkerem</title>
        <meta charset="utf-8">
    </head>
    <body>
        <h1>Společné psaní básně s Wolkerem</h1>
        <p>Jsem GenZ Wolker 2, mladý Jiří Wolker v moderním světě, vždy odkazující na své znalosti.</p>
""")

if topic:
    # už máme téma
    if content:
        # pokračujem
        prompt = '\n'.join((f'Báseň na téma: {topic}', content, verse1, verse2, 'Napiš další dva řádky básně:'))
        continuation = talk(prompt)
        content = '\n'.join((content, verse1, verse2, continuation))
    else:
        # začínáme
        prompt = f"Napiš první dva řádky básně na téma: {topic}"
        content = talk(prompt)
else:
    # ještě nemáme ani téma
    content = None

if content:
    content_html = content.replace('\n', '<br>')
    print(f"""
        <h2>Báseň na téma {topic}</h2>
        <p>{content_html}</p>
        <p>...</p>
        <h2>Dál je to na tobě! Vymysli další dva verše, tak aby se báseň rýmovala:</h2>
        <form method="post">
            <input name="verse1" size="50"><br>
            <input name="verse2" size="50"><br>
            <input type="hidden" name="topic" value="{topic}">
            <input type="hidden" name="content" value="{content}">
            <input type="submit" value="Pokračovat">
        </form>
        <hr>
        <input disabled type="submit" value="Takhle je to hotové, sdílet!">
        <hr>
        </body>
        </html>
        """)
else:
    print(f"""
        <h2>Na jaké téma chceš společně s Wolkerem psát báseň?</h2>
        <form method="post">
            {' '.join([ f'<input type="submit" name="topic" value="{opt}"><br>' for opt in options])}
        </form>
        <form method="post">
            <input name="topic_freeform"> <input type="submit" value="Jdeme psát">
        </form>
        </body>
        </html>
        """)

