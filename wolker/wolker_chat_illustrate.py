#!/usr/bin/env python3
#coding: utf-8

import cgi
import common

common.httpheader()
form = cgi.FieldStorage()
replacements = common.get_replacements(form)
print(*common.wolker_chat_illustrate(form, replacements), sep='\n')
