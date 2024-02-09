#!/usr/bin/env python3
#coding: utf-8

import common
import os
import cgi

def append(files, filename):
    files.append(common.return_file(filename))
    
def main(typ=''):
    files = []
    append(files, 'header.html')
    
    if typ == 'admin':
        append(files, 'gallery_admin_head.html')
    append(files, 'gallery_head.html')

    postfiles = os.listdir('genouts')
    postfiles.sort(reverse=True)
    for filename in postfiles:
        append(files, f'genouts/{filename}')
        if typ == 'admin':
            key, _ = filename.split('.')
            files.append(common.replace_and_return_file(
                    'gallery_admin_sharebutton.html', {'KEY': key}))
        
            append(files, 'gallery_sep.html')
    append(files, 'footer.html')
    
    return files

if __name__=="__main__":
    form = cgi.FieldStorage()
    typ = form.getvalue("typ", "")
    
    common.httpheader()
    print(*main(typ), sep='\n')
