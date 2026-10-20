#!/bin/bash
# Called by autodeploy.sh after a git merge. Restarts every EduPo process.
# No root needed: each process is killed and systemd (Restart=always,
# RestartSec=10) -- or the old while-loop scripts -- starts it again with the
# new code and, for gunicorn, the new command line from start-backend.sh.

source ~/.bashrc
echo Restart generators...
pkill -e -f 'python3 gen.py'
echo Restart analysis worker...
pkill -e -f 'python3 analyze.py'
echo Restart backend server...
# TERM (not HUP): a HUP only reloads the app code, keeping the old gunicorn
# command line and environment. Expect ~10-20 s of downtime while systemd
# restarts it.
kill -TERM $(cat gunicorn.pid)
