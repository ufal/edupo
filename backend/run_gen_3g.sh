#!/bin/bash

f=$(date "+%Y-%m-%d-%H-%M-%S")
l=logs/gen_tm.log

T=10s

echo Starting NEW generator loop, logs in $l, autorestart in $T

source ~/.bashrc
while true;
do
    date
    echo Starting/reloading New generator model...
    python3 gen.py new 5012 --16bit
    echo Generator stopped, waiting $T for restart...
    sleep $T
    echo
done >> $l 2>&1

