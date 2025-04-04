#!/bin/bash

source ~/.bashrc
echo Reload generators...
pkill -e -f gen.py
python3 gen.py mc 5010 &>> logs/gen_mc.log &
python3 gen.py tm 5011 &>> logs/gen_tm.log &
echo Reload backend server...
kill -HUP $(cat gunicorn.pid)

