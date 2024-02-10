#!/usr/bin/env python3
#coding: utf-8

import common
import cgi
common.httpheader()
form = cgi.FieldStorage()
title = form.getvalue("title", "")
text = form.getvalue("text", "")
print(*common.wolker_feel(title, text), sep='\n')
