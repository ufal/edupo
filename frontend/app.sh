#!/bin/bash

f=$(date "+%Y-%m-%d-%H-%M-%S")
l=logs/app.$f.log

T=10s

echo Starting frontend server loop, logs in $l, autorestart in $T

while true;
do
    date
    echo Starting frontend server...
    EDUPO_SERVER_PATH=/edupo authbind --deep gunicorn app:app -b 0.0.0.0:80 -w 3 --access-logfile=- --pid gunicorn.pid
    echo Frontend server stopped, waiting $T for restart...
    sleep $T
    echo
done > $l 2>&1

# requires sudo:
# flask run --host=0.0.0.0 --port 80
# debug run:
# flask run --host=0.0.0.0 --debug

