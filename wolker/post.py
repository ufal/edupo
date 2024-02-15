#!/usr/bin/env python3
#coding: utf-8

import common
import cgi

common.httpheader()
form = cgi.FieldStorage()
key = form.getvalue("key", "")
print(*common.post(key), sep="\n")
