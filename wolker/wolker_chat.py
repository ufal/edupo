#!/usr/bin/env python3
#coding: utf-8

import cgi
import common

if __name__=="__main__":
    common.httpheader()
    form = cgi.FieldStorage()
    text = form.getvalue("text", "")
    assistant_id = form.getvalue('assistant_id', 'asst_oEwl7wnhGDi5JDvAdE92GgWk')
    thread_id = form.getvalue("thread_id", None)
    print(*common.wolker_chat(text, assistant_id, thread_id), sep='\n')
