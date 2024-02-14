#!/usr/bin/env python3
#coding: utf-8

import cgi
import common

if __name__=="__main__":
    common.httpheader()
    form = cgi.FieldStorage()
    text = form.getvalue("text", "")
    typ = form.getvalue("typ", "poem")
    title = form.getvalue("title", "")
    thread_id = form.getvalue("thread_id", None)
    print(*common.wolker_chat(text, typ, title, thread_id), sep='\n')
