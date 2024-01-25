#!/usr/bin/env python3
#coding: utf-8

import sys
import cgi
from wolker_interactive import talk


print("Content-type: text/html")
print()

form = cgi.FieldStorage()
text = form.getvalue("text", None)
prompt = form.getvalue("prompt", None)

if prompt and not text:
    text = prompt

if text:
    response = talk(text).replace('\n', '<br>')


print(f"""
<!DOCTYPE html>
    <html lang="cs">
    <head>
        <title>Povídání s Wolkerem</title>
        <meta charset="utf-8">
    </head>
    <body>
        <h1>Povídání s Wolkerem</h1>
        <p>Jsem GenZ Wolker 2, mladý Jiří Wolker v moderním světě, vždy odkazující na své znalosti.</p>
        <p>(Teď to nedrží kontext konverzace, každou zprávu to zpracovává
        nezávisle. Ale to se dá případně upravit aby to vedlo jednou souvislou
        konverzaci. Ale možná je to takhle OK.)</p>
""")
        
if text and response:
    print(f"""
    <h2>{text}</h2>
    <p>{response}</p>
    <input disabled type="submit" value="Sdílet">
    <hr>
    """)


options = [
        "Podělte své myšlenky o moderní poezii.",
        "Popište dnešní svět ve svém poetickém stylu.",
        "Napište báseň o přírodě ve městě.",
        "Co v dnešní společnosti vás inspiruje k vaší poezii?",
        ]

print(f"""
        <h2>Řekněte něco GenZ Wolkerovi!</h2>
        <form method="post">
            {' '.join([ f'<input type="submit" name="text" value="{opt}"><br>' for opt in options])}
            <input name="prompt"> <input type="submit" value="Říct">
        </form>
        </body>
        </html>
        """)


