#!/bin/bash

# debug run
# run only on local computer, not visible from outside
EDUPO_API_URL='https://quest.ms.mff.cuni.cz/edupo-api/' flask run --debug --port=5001

# debug VISIBLE FROM OUTSIDE
# (run this only if you know what are doing)
# flask run --host=0.0.0.0 --debug

