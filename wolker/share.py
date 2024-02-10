#!/usr/bin/env python3
#coding: utf-8

import cgi
import common

common.httpheader()
cgiform = cgi.FieldStorage()
form = {}
for field in ['thread_id', 'title', 'text', 'image', 'author']:
    form[field] = cgiform.getvalue(field, '')
print(*common.share_page(form), sep='\n')

