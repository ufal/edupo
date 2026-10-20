# EduPo systemd deployment

Systemd units replacing the screen/while-loop setup on the production server
(`edupo`, user `jarda`). One unit per component, matching what runs today:

| unit | replaces | what it runs |
|---|---|---|
| `edupo-backend.service` | `backend/app.sh` loop | gunicorn `app:app` on port 5000, 2 workers |
| `edupo-gen-mc.service` | `backend/run_gen_mc.sh` loop | `gen.py mc 5010` (ZMQ) |
| `edupo-gen-tm.service` | `backend/run_gen_tm.sh` loop | `gen.py tm 5011 --16bit` (ZMQ) |
| `edupo-gen-new.service` | `backend/run_gen_3g.sh` loop | `gen.py new 5012 --16bit` — optional, only if the `new` modelspec is in use |
| `edupo-analyze.service` | (new; analysis used to run inside gunicorn) | `analyze.py 5013` (ZMQ) — kveta + measures worker, required by `/analyze`, poem display and multi-try generation |
| `edupo-autodeploy.timer` + `.service` | cron entry | `autodeploy.sh` every minute |

The frontend (Next.js under pm2) is deliberately not covered for now and is
left running as it is.

The units call the `start-*.sh` launchers in this directory; server-specific
paths live in one place, `env.sh`. Restart-on-crash with a 10s delay is
handled by systemd (`Restart=always`, `RestartSec=10`), same behaviour as the
old while loops. `authbind` was dropped — port 5000 doesn't need it.

`autodeploy.sh` and `reload.sh` keep working unchanged: `pkill -f gen.py`
makes systemd restart the generators, and `kill -HUP` on the gunicorn pid
file gracefully reloads the backend workers. `systemctl reload
edupo-backend` does the same HUP.

Not covered here (unchanged): the frontend, the reverse proxy in front of
port 5000, frontend-lite (static files, no process), the data directory
`/net/projects/EduPo/data/` (new.db, cache.db, apikey.txt, hesla.json).

## Installation (on the server, once)

1. **Set the paths.** Edit `deploy/env.sh`: repo checkout path and Python
   env bin dir (`conda activate edupo; dirname "$(which python3)"`).

2. **Fix paths in the unit files** if the repo is not at `/home/jarda/edupo`:

   ```bash
   sed -i 's#/home/jarda/edupo#/actual/path/to/edupo#g' deploy/systemd/*.service
   ```

   (Unit files can't read `env.sh`, so the launcher path is hardcoded there.)

3. **Install the units:**

   ```bash
   sudo cp deploy/systemd/edupo-*.service deploy/systemd/edupo-*.timer /etc/systemd/system/
   sudo systemctl daemon-reload
   ```

4. **Stop the old setup** (avoid double instances):
   - `screen -ls` and kill the sessions running `app.sh`, `run_gen_mc.sh`,
     `run_gen_tm.sh` (or `pkill -f app.sh` etc., then `pkill -f gunicorn`,
     `pkill -f gen.py`).
   - `crontab -e` and remove/comment the `autodeploy.sh` line.

5. **Start and enable** (`enable` also makes them start on server boot):

   ```bash
   sudo systemctl enable --now edupo-gen-mc edupo-gen-tm edupo-analyze edupo-backend
   sudo systemctl enable --now edupo-autodeploy.timer
   ```

6. **Check:**

   ```bash
   systemctl status 'edupo-*'
   curl -s localhost:5000/prdel?accept=txt
   ```

## Day-to-day

- logs stay where they always were — `backend/logs/app.<date>.log` (a new
  dated file per backend (re)start), `backend/logs/gen_mc.log`,
  `backend/logs/gen_tm.log`, `backend/logs/analyze.log`, `autodeploy.log` — so `watch_server.sh` keeps
  working. The journal (`journalctl -u edupo-backend` etc.) only catches
  launcher-level errors, e.g. wrong paths in `env.sh`.
- reload backend code without dropping requests: `sudo systemctl reload edupo-backend`
- restart a generator: `sudo systemctl restart edupo-gen-tm`
- restart the analysis worker (after changes under `kveta/`): `sudo systemctl restart edupo-analyze`
- deploys still happen automatically via the timer;
  run one manually: `sudo systemctl start edupo-autodeploy.service`

## If you have no root on the server

Same units work as user units: drop the `User=` lines, put them in
`~/.config/systemd/user/`, change `WantedBy=multi-user.target` to
`WantedBy=default.target`, use `systemctl --user ...` for everything, and run
`sudo loginctl enable-linger jarda` once (this one does need root) so they
survive logout and start on boot.
