#!/usr/bin/env python3
#coding: utf-8

import common
import os
import cgi

common.header()

form = cgi.FieldStorage()
key = form.getvalue("key", "")
filename = f'genouts/{key}.html'

if key and key.isnumeric() and os.path.isfile(filename):
    common.write_out_file(filename)
else:
    print(f"Nelze zobrazit soubor se zadaným klíčem '{key}'")

common.footer()
