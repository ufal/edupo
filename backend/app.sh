#!/bin/bash

f=$(date "+%Y-%m-%d-%H-%M-%S")
l=logs/app.$f.log

T=10s

echo Starting backend server loop, logs in $l, autorestart in $T

while true;
do
    date
    echo Starting backend server...
    EDUPO_SERVER_PATH=/edupo-api authbind --deep gunicorn app:app -b 0.0.0.0:5000 -w 2 --access-logfile=- --pid gunicorn.pid
    echo Backend server stopped, waiting $T for restart...
    sleep $T
    echo
done > $l 2>&1
