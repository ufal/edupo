#!/usr/bin/env python3
#coding: utf-8

import cgi
import common

if __name__=="__main__":
    common.httpheader()
    form = cgi.FieldStorage()
    title = form.getvalue("title", "")
    prefix = form.getvalue("prefix", "")
    text = form.getvalue("text", "")
    replacements = common.get_replacements(
            form, ['image', 'thread_id', 'text', 'title', 'back'])
    print(*common.wolker_image(title, prefix, text, replacements), sep='\n')

