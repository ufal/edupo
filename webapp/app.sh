#!/bin/bash

f=$(date "+%Y-%m-%d-%H-%M-%S")
l=app.$f.log
e=app.$f.err

T=10s

while true;
do
    echo Starting server, logs in $l and $e
    authbind --deep flask run --host=0.0.0.0 --port 80
    echo Server stopped, waiting $T for restart...
    sleep $T
done > $l 2> $e

# requires sudo:
# flask run --host=0.0.0.0 --port 80
# debug run:
# flask run --host=0.0.0.0 --debug

