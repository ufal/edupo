#!/bin/bash
# Launched by the edupo-gen-*.service units:
#   start-gen.sh <modelspec> <port> [extra args...]
# e.g. start-gen.sh mc 5010
#      start-gen.sh tm 5011 --16bit

source "$(dirname "$(readlink -f "$0")")/env.sh"
cd "$REPO/backend"

# Log to the same files as the run_gen_*.sh loops did (logs/gen_mc.log etc.).
exec >> "logs/gen_$1.log" 2>&1
date
echo "Starting/reloading $1 generator model..."

exec "$PYBIN/python3" gen.py "$@"
