#!/usr/bin/env python3
#coding: utf-8

import sys
import cgi
import wolker_interactive
import common

common.header()

form = cgi.FieldStorage()
typ = form.getvalue("typ", "")
prefix = form.getvalue("prefix", "")
text = form.getvalue("text", "")
thread_id = form.getvalue("thread_id", None)

# TODO check if data filled in

message = prefix + text
messages, roles, thread_id = wolker_interactive.talk_threaded(message, thread_id)

for message, role in zip(messages, roles):
    # role is user or assistant
    print(f'<p class="{role}">{common.nl2br(message)}</p>')

print(f"""
    <form method="post">
        <textarea name="text" rows="4" cols="60"></textarea>
        <input type="hidden" name="typ" value="{typ}">
        <input type="hidden" name="thread_id" value="{thread_id}">
        <br>
        <input type="submit" value="Odpovědět">
    </form>
    """)

print('<br><hr><br>')

print(f"""
    <form method="post" action="share.py">
        <p>
        Text můžeš veřejně sdílet v Galerii; promítne se v muzeu a bude vidět online!
        <input type="hidden" name="typ" value="thread">
        <input type="hidden" name="thread_id" value="{thread_id}">
        <input type="submit" value="Sdílet text bez obrázku">
        </p>
    </form>
    """)

print('<br><hr><br>')

# TODO umožnit se sem pak ještě vrátit k úpravě popisiku obrázku?
print(f"""
    <form method="post" action="wolker_image.py">
        <input type="hidden" name="typ" value="thread">
        <input type="hidden" name="thread_id" value="{thread_id}">
        <input type="hidden" name="prefix" value="Image accompanying a poetic generated text, as a conversation between the user and a young Czech poet from the beginning on the 20th century.  ">
        Popis doprovodného obrázku: <input name="text" size=50>
        <input name="submit" type="submit" value="Vytvoř k textu obrázek">
    </form>
    """)

# Pokračovat dál v konverzaci:
# Skončenou konverzaci můžeš veřejně sdílet v Galerii; promítne se v muzeu a bude vidět online!
# Ke skončené konverzaci můžeš vygenerovat obrázek!
# Popište několika slovy nebo několika větami, jak by měl vypadat obrázek k této konverzaci:

common.footer()
