#!/bin/bash
# Launched by edupo-backend.service.
# Equivalent of backend/app.sh without the restart loop (systemd handles
# restarts) and without authbind (port 5000 is unprivileged).

source "$(dirname "$(readlink -f "$0")")/env.sh"
cd "$REPO/backend"

# Log to the same place as app.sh did: a dated file in backend/logs/
# (one file per service (re)start; watch_server.sh tails the newest one).
f=$(date "+%Y-%m-%d-%H-%M-%S")
exec >> "logs/app.$f.log" 2>&1
date
echo Starting backend server...

export EDUPO_CACHE_MAX_REGEN_IN_FLIGHT=3
export EDUPO_SERVER_PATH=/api

exec "$PYBIN/gunicorn" app:app -b 0.0.0.0:5000 -w 2 \
    --access-logfile=- \
    --access-logformat '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" [%({x-request-id}o)s]' \
    --pid gunicorn.pid \
    --timeout 180
