#!/bin/bash
# Launched by the edupo-gen-*.service units:
#   start-gen.sh <modelspec> <port> [extra args...]
# e.g. start-gen.sh new 5012 --16bit

source "$(dirname "$(readlink -f "$0")")/env.sh"
cd "$REPO/backend"

# Log to the same files as the run_gen_*.sh loops did (logs/gen_new.log).
exec >> "logs/gen_$1.log" 2>&1
date
echo "Starting/reloading $1 generator model..."

exec "$PYBIN/python3" gen.py "$@"
