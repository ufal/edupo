#!/usr/bin/env python3
#coding: utf-8

import common
import cgi

form = cgi.FieldStorage()
typ = form.getvalue("typ", "")

common.httpheader()
print(*common.gallery(typ), sep='\n')
