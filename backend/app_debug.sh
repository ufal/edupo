#!/bin/bash

# debug run
# run only on local computer, not visible from outside
echo "Starting/reloading analysis worker..."

exec python3 analyze.py "$@" & 
flask run --debug

# debug VISIBLE FROM OUTSIDE
# (run this only if you know what are doing)
# flask run --host=0.0.0.0 --debug

