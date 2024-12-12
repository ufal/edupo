#!/bin/bash

# debug run
# run only on local computer, not visible from outside
flask run --debug

# debug VISIBLE FROM OUTSIDE
# (run this only if you know what are doing)
# flask run --host=0.0.0.0 --debug

