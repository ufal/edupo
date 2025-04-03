#!/bin/bash

f=$(date "+%Y-%m-%d-%H-%M-%S")
l=logs/app.$f.log

T=10s

echo Starting backend server loop, logs in $l, autorestart in $T

while true;
do
    date
    echo Starting generator models...
    python3 gen.py mc 5010 2>> logs/gen_mc.log &
    mcpid=$!
    python3 gen.py tm 5011 2>> logs/gen_tm.log &
    tmpid=$!
    echo Starting backend server...
    # TODO explicitly set MC_MODEL_PORT and TM_MODEL_PORT?
    EDUPO_SERVER_PATH=/edupo-api authbind --deep gunicorn app:app -b 0.0.0.0:5000 -w 2 --access-logfile=- --pid gunicorn.pid --timeout 180
    echo Backend server stopped, killing generator models and waiting $T for restart...
    kill $mcpid
    kill $tmpid
    sleep $T
    echo
done > $l 2>&1
