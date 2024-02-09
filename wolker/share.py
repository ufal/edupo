#!/usr/bin/env python3
#coding: utf-8

import cgi
import common

if __name__=="__main__":
    common.httpheader()
    form = cgi.FieldStorage()
    print(*common.share_page(form), sep='\n')

