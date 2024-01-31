#!/usr/bin/env python3
#coding: utf-8

import cgi
import common

common.header()

form = cgi.FieldStorage()
text = form.getvalue("text", "")
title = form.getvalue("title", "")
replacements = {'TEXT': text, 'TITLE': title}

common.replace_and_write_out_file('welcome_wolker_feel.html', replacements)

common.footer()
