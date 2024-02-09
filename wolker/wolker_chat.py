#!/usr/bin/env python3
#coding: utf-8

import cgi
import wolker_interactive
import common

common.header()

# input parameters
form = cgi.FieldStorage()
text = form.getvalue("text", "")
assistant_id = form.getvalue('assistant_id', 'asst_oEwl7wnhGDi5JDvAdE92GgWk')
thread_id = form.getvalue("thread_id", None)

# invoke the chatbot
messages, roles, thread_id = wolker_interactive.talk_threaded(
        text, assistant_id, thread_id)

# compose the page
common.replace_and_write_out_file('wolker_chat_head.html', {})
for message, role in zip(messages, roles):
    # role is user or assistant
    common.replace_and_write_out_file(f'wolker_chat_message_{role}.html',
            {'CONTENT': common.nl2br(message)})
common.replace_and_write_out_file('wolker_chat_controls.html',
        {'THREAD_ID': thread_id, 'ASSISTANT_ID': assistant_id})

common.footer()
