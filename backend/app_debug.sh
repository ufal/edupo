#!/bin/bash

# debug run
# run only on local computer, not visible from outside
echo "Starting/reloading analysis worker..."
python3 analyze.py "$@" &
echo Starting generator model...
python3 gen.py new 5012 --16bit &
echo new model process id $!
echo Starting Flask...
flask run --debug

# debug VISIBLE FROM OUTSIDE
# (run this only if you know what are doing)
# flask run --host=0.0.0.0 --debug

