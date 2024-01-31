#!/usr/bin/env python3
#coding: utf-8

import cgi
import common

common.header()

form = cgi.FieldStorage()
text = form.getvalue("text", "")
replacements = {'TEXT': text}

common.replace_and_write_out_file('welcome_wolker_image.html', replacements)

common.footer()
