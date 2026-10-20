#!/bin/bash
# Launched by edupo-analyze.service:
#   start-analyze.sh [port]     (default 5013)

source "$(dirname "$(readlink -f "$0")")/env.sh"
cd "$REPO/backend"

exec >> "logs/analyze.log" 2>&1
date
echo "Starting/reloading analysis worker..."

exec "$PYBIN/python3" analyze.py "$@"
