#!/bin/bash

f=$(date "+%Y-%m-%d-%H-%M-%S")
l=logs/app.$f.log

T=10s

echo Starting server loop, logs in $l, autorestart in $T

while true;
do
    date
    echo Starting server...
    authbind --deep flask run --host=0.0.0.0 --port 80
    echo Server stopped, waiting $T for restart...
    sleep $T
    echo
done > $l 2>&1

# requires sudo:
# flask run --host=0.0.0.0 --port 80
# debug run:
# flask run --host=0.0.0.0 --debug

