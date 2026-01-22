#!/bin/bash

# debug run
# run only on local computer, not visible from outside
echo Starting generator models...
python3 gen.py mc 5010 &
python3 gen.py new 5012 &
echo mc process id $!
echo Starting Flask...
flask run --debug

# debug VISIBLE FROM OUTSIDE
# (run this only if you know what are doing)
# flask run --host=0.0.0.0 --debug

