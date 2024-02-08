#!/usr/bin/env python3
#coding: utf-8

import cgi
import common

common.header()

replacements = common.get_replacements(
        ['text', 'task', 'taskshort', 'assistant_id'])

common.replace_and_write_out_file('welcome_wolker_chat_topic.html', replacements)

common.footer()
