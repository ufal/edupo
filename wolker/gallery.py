#!/usr/bin/env python3
#coding: utf-8

import common
import cgi

if __name__=="__main__":
    form = cgi.FieldStorage()
    typ = form.getvalue("typ", "")
    
    common.httpheader()
    print(*common.gallery(typ), sep='\n')
