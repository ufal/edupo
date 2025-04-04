#!/bin/bash

echo Reload generators...
pgrep -e -a -f gen.py
python3 gen.py mc 5010 2>> logs/gen_mc.log &
python3 gen.py tm 5011 2>> logs/gen_tm.log &
echo Reload backend server...
kill -HUP $(cat gunicorn.pid)

