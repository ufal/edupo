#!/bin/bash

f=$(date "+%Y-%m-%d-%H-%M-%S")
l=logs/gen_mc.log

T=10s

echo Starting MC generator loop, logs in $l, autorestart in $T

source ~/.bashrc
while true;
do
    date
    echo Starting/reloading MC generator model...
    python3 gen.py mc 5010
    echo Generator stopped, waiting $T for restart...
    sleep $T
    echo
done >> $l 2>&1

