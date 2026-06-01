#!/usr/bin/env python3
# coding: utf-8
"""
Poem caching for limited, predetermined frontends (e.g. the "lite" frontend at
edupo.digitalneumenia.sk).

Such a frontend offers only a small fixed set of generation parameters, so we can
serve a previously generated poem instantly and regenerate a fresh one in the
background. This makes generation instant and shields the frontend from OpenRouter
outages / long backend queues.

Cached poems live in a SEPARATE SQLite database (CACHE_DBFILE), independent of the
read-only corpus DB. This module must work OUTSIDE of any Flask request/app context
(the background regeneration runs in a daemon thread), so it never touches Flask `g`
and opens its own short-lived connections.

Serving algorithm (per parameter combination, identified by a canonical cache key):
  * each key has an ordered list of poems (cache_poems) and a next_index (cache_state)
  * a request serves poems[next_index % n], advances next_index, and -- if no
    regeneration is already in flight for that key -- spawns one background regen
  * when requests outrun generation the index wraps ("restarts"), cycling through the
    cached poems; worst case the same poems repeat, but the user always gets one instantly
  * we keep ALL generated poems (no eviction)

The cache-key derivation (cache_key_for) is FROZEN and deterministic so a separate
warm-up import script can reproduce the exact same keys.
"""

import hashlib
import json
import logging
import os
import sqlite3
import threading
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

CACHE_DBFILE = os.getenv('EDUPO_CACHE_DB', '/net/projects/EduPo/data/cache.db')

# A regeneration slot is considered stale (and may be reclaimed) after this many
# seconds. Must be comfortably above gunicorn's --timeout (180s) so a worker that was
# killed/recycled mid-generation does not strand the flag forever.
GENERATING_STALE_SECONDS = 300

# Cap on concurrent background regenerations per cache key.
#   1 (default): at most one regen per key at a time. Cheap, safe under bursts, but the
#                cache fills slowly when traffic is heavy (most requests find a regen
#                already in flight and skip spawning).
#   0         : unlimited -- every cache hit spawns its own regen. Cache fills faster, at
#                the cost of N parallel OpenRouter calls per traffic burst (rate-limit
#                risk, N-times cost).
# Override via EDUPO_CACHE_MAX_REGEN_IN_FLIGHT.
MAX_REGEN_IN_FLIGHT = int(os.getenv('EDUPO_CACHE_MAX_REGEN_IN_FLIGHT', '1'))

# FROZEN: the generation-relevant fields that define a cache key. The warm-up import
# script must use the exact same list and normalization (see cache_key_for).
CACHE_KEY_FIELDS = [
    'modelspec', 'temperature', 'poem_length', 'syllables_count',
    'motives', 'mood', 'old_style', 'rhymed', 'rhyme_scheme', 'verses_count',
]

_SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS cache_state (
    cache_key        TEXT PRIMARY KEY,
    gen_params_json  TEXT,
    next_index       INTEGER NOT NULL DEFAULT 0,
    generating       INTEGER NOT NULL DEFAULT 0,
    generating_since TEXT,
    last_accessed    TEXT
);
CREATE TABLE IF NOT EXISTS cache_poems (
    seq        INTEGER PRIMARY KEY AUTOINCREMENT,
    cache_key  TEXT NOT NULL,
    poemid     TEXT NOT NULL,
    poem_json  TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_cache_poems_key ON cache_poems(cache_key, seq);
-- one row per currently-running background regeneration (observability for /cache_stats)
CREATE TABLE IF NOT EXISTS cache_in_flight (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    cache_key  TEXT NOT NULL,
    started_at TEXT NOT NULL,
    pid        INTEGER
);
CREATE INDEX IF NOT EXISTS idx_cache_in_flight_started ON cache_in_flight(started_at);
"""


def _connect():
    # isolation_level=None -> autocommit; we manage transactions explicitly with
    # BEGIN IMMEDIATE where we need a write lock.
    conn = sqlite3.connect(CACHE_DBFILE, timeout=10, isolation_level=None)
    conn.execute("PRAGMA busy_timeout=5000")
    return conn


def init_cache_db():
    """Create the cache DB / tables if needed. Safe to call from every worker at
    import time (CREATE ... IF NOT EXISTS). Enables WAL so the read-heavy hit path
    does not block on background writers."""
    conn = _connect()
    try:
        conn.execute("PRAGMA journal_mode=WAL")
        conn.executescript(_SCHEMA_SQL)
        # Additive migration: cache_state.last_accessed was added after the initial
        # release; add the column on pre-existing DBs.
        cols = {r[1] for r in conn.execute("PRAGMA table_info(cache_state)")}
        if 'last_accessed' not in cols:
            conn.execute("ALTER TABLE cache_state ADD COLUMN last_accessed TEXT")
    finally:
        conn.close()


def cache_key_for(params):
    """Return a deterministic SHA-256 hex key for the generation-relevant params.

    FROZEN derivation -- keep in sync with the warm-up import script:
      * temperature -> round(float, 3)
      * motives     -> stripped, empties dropped, sorted (order-insensitive)
      * everything else used as-is
      * canonical JSON with sorted keys
    """
    fields = {}
    for f in CACHE_KEY_FIELDS:
        v = params.get(f)
        if f == 'temperature':
            try:
                v = round(float(v), 3)
            except (TypeError, ValueError):
                pass
        elif f == 'motives':
            if isinstance(v, (list, tuple)):
                v = sorted(m.strip() for m in v if m and str(m).strip())
            elif isinstance(v, str):
                v = sorted(m.strip() for m in v.split('\n') if m.strip())
            else:
                v = []
        fields[f] = v
    key_json = json.dumps(fields, sort_keys=True, ensure_ascii=False, separators=(',', ':'))
    return hashlib.sha256(key_json.encode('utf-8')).hexdigest()


def _is_stale(generating_since_iso, now):
    if not generating_since_iso:
        return True
    try:
        since = datetime.fromisoformat(generating_since_iso)
    except (TypeError, ValueError):
        return True
    return (now - since).total_seconds() > GENERATING_STALE_SECONDS


def _store_generated(key, params, data, set_next_index_to=None):
    """Insert a freshly generated poem into cache_poems. If set_next_index_to is not
    None, also upsert cache_state with the given next_index AND last_accessed=now (this
    code path runs on a cache miss, which is itself a request, so it counts as an access).
    gen_params_json holds the FULL params dict so the background regen has everything it
    needs (modelspec, max_tries, min_meaning, max_unk, ...)."""
    poem_json = json.dumps(data, ensure_ascii=False)
    poemid = data.get('id', '')
    conn = _connect()
    try:
        conn.execute("BEGIN IMMEDIATE")
        conn.execute(
            "INSERT INTO cache_poems(cache_key, poemid, poem_json) VALUES (?,?,?)",
            (key, poemid, poem_json))
        if set_next_index_to is not None:
            now_iso = datetime.utcnow().isoformat()
            conn.execute(
                "INSERT INTO cache_state(cache_key, gen_params_json, next_index, generating, generating_since, last_accessed) "
                "VALUES (?,?,?,0,NULL,?) "
                "ON CONFLICT(cache_key) DO UPDATE SET "
                "  gen_params_json=excluded.gen_params_json, next_index=excluded.next_index, "
                "  last_accessed=excluded.last_accessed",
                (key, json.dumps(params, ensure_ascii=False), set_next_index_to, now_iso))
        conn.execute("COMMIT")
    finally:
        conn.close()


def _clear_generating(key):
    conn = _connect()
    try:
        conn.execute(
            "UPDATE cache_state SET generating=0, generating_since=NULL WHERE cache_key=?",
            (key,))
    finally:
        conn.close()


def _begin_flight(key):
    """Record a now-starting background regen. Returns the row id used by _end_flight.
    Purely observational -- the single-flight gate is still driven by cache_state.generating."""
    conn = _connect()
    try:
        cur = conn.execute(
            "INSERT INTO cache_in_flight(cache_key, started_at, pid) VALUES (?,?,?)",
            (key, datetime.utcnow().isoformat(), os.getpid()))
        return cur.lastrowid
    finally:
        conn.close()


def _end_flight(flight_id):
    conn = _connect()
    try:
        conn.execute("DELETE FROM cache_in_flight WHERE id=?", (flight_id,))
    finally:
        conn.close()


def _bg_regen(key, params, generate_fn):
    """Background daemon-thread body: generate a fresh poem and append it to the pool.
    Always clears the `generating` flag and the in-flight row, even on failure (e.g.
    OpenRouter down), so the key is not stranded."""
    flight_id = _begin_flight(key)
    try:
        data = generate_fn(params)  # generates + assigns id (no poemfile for cached frontends)
        _store_generated(key, params, data)
        logger.info("Background regen stored poem %s for cache_key=%s", data.get('id'), key)
    except Exception:
        logger.exception("Background poem regen failed for cache_key=%s", key)
    finally:
        _end_flight(flight_id)
        _clear_generating(key)


def _spawn_regen(key, params, generate_fn):
    threading.Thread(
        target=_bg_regen, args=(key, params, generate_fn), daemon=True).start()


def serve_from_cache(params, generate_fn):
    """Serve a cached poem for `params`, refreshing the cache in the background.

    `generate_fn(params) -> data` is the synchronous generator (app.generuj_poem); it
    is passed in to avoid a circular import. Returns the `data` dict (same shape the
    normal /gen path produces).
    """
    key = cache_key_for(params)
    now = datetime.utcnow()

    conn = _connect()
    try:
        conn.execute("BEGIN IMMEDIATE")
        n = conn.execute(
            "SELECT COUNT(*) FROM cache_poems WHERE cache_key=?", (key,)).fetchone()[0]

        if n == 0:
            # Cache miss: don't hold the write lock across the slow generation.
            conn.execute("COMMIT")
            conn.close()
            conn = None
            logger.info("Cache MISS for cache_key=%s -- generating synchronously", key)
            data = generate_fn(params)
            _store_generated(key, params, data, set_next_index_to=1)
            return data

        # Cache hit: pick poems[next_index % n], advance the index, claim the regen slot.
        row = conn.execute(
            "SELECT next_index, generating, generating_since FROM cache_state WHERE cache_key=?",
            (key,)).fetchone()
        next_index = row[0] if row else 0
        generating = row[1] if row else 0
        gsince = row[2] if row else None

        idx = next_index % n
        poem_json = conn.execute(
            "SELECT poem_json FROM cache_poems WHERE cache_key=? ORDER BY seq LIMIT 1 OFFSET ?",
            (key, idx)).fetchone()[0]
        data = json.loads(poem_json)

        # MAX_REGEN_IN_FLIGHT==0 disables the single-flight gate: every hit spawns a regen.
        if MAX_REGEN_IN_FLIGHT == 0:
            claim = True
        else:
            claim = (not generating) or _is_stale(gsince, now)
        new_next = idx + 1
        new_generating = 1 if claim else generating
        new_since = now.isoformat() if claim else gsince

        now_iso = now.isoformat()
        if row:
            conn.execute(
                "UPDATE cache_state SET next_index=?, generating=?, generating_since=?, last_accessed=? WHERE cache_key=?",
                (new_next, new_generating, new_since, now_iso, key))
        else:
            # Poems exist but no state row yet (e.g. warm-up import only populated
            # cache_poems): create the state row using the current request's params.
            conn.execute(
                "INSERT INTO cache_state(cache_key, gen_params_json, next_index, generating, generating_since, last_accessed) "
                "VALUES (?,?,?,?,?,?)",
                (key, json.dumps(params, ensure_ascii=False), new_next, new_generating, new_since, now_iso))
        conn.execute("COMMIT")
    except Exception:
        if conn is not None:
            try:
                conn.execute("ROLLBACK")
            except sqlite3.Error:
                pass
        raise
    finally:
        if conn is not None:
            conn.close()

    if claim:
        _spawn_regen(key, params, generate_fn)
    return data


# ---------------------------------------------------------------------------
# Stats (for the /cache_stats endpoint)
# ---------------------------------------------------------------------------

# Fields rendered by short_params(), in display order. Anything else in the params blob
# (max_tries, min_meaning, ...) is omitted to keep the line compact.
_SHORT_PARAM_FIELDS = (
    'modelspec', 'temperature', 'old_style', 'syllables_count', 'poem_length',
    'verses_count', 'rhyme_scheme', 'rhymed', 'mood', 'motives',
)


def short_params(params_json):
    """Compact one-line summary of a gen_params_json blob: drops empty/zero values and
    renders each remaining field as `key=value`. Used by /cache_stats."""
    if not params_json:
        return ""
    try:
        p = json.loads(params_json)
    except (TypeError, ValueError):
        return params_json
    parts = []
    for k in _SHORT_PARAM_FIELDS:
        v = p.get(k)
        if v in (None, '', 0, [], {}):
            continue
        if isinstance(v, (list, tuple)):
            v = '+'.join(str(x) for x in v)
        parts.append(f"{k}={v}")
    return " ".join(parts)


def stats():
    """Snapshot of cache contents and activity for /cache_stats. Single short-lived
    connection; only reads except for opportunistic stranded-row filtering via WHERE."""
    cutoff = (datetime.utcnow() - timedelta(seconds=GENERATING_STALE_SECONDS)).isoformat()
    conn = _connect()
    try:
        running = conn.execute(
            "SELECT COUNT(*) FROM cache_in_flight WHERE started_at > ?", (cutoff,)
        ).fetchone()[0]
        total_poems = conn.execute("SELECT COUNT(*) FROM cache_poems").fetchone()[0]
        distinct_combos = conn.execute(
            "SELECT COUNT(DISTINCT cache_key) FROM cache_poems").fetchone()[0]
        starved = conn.execute(
            "SELECT COUNT(*) FROM (SELECT cache_key FROM cache_poems "
            "GROUP BY cache_key HAVING COUNT(*) = 1)").fetchone()[0]
        oldest, newest = conn.execute(
            "SELECT MIN(created_at), MAX(created_at) FROM cache_poems").fetchone()
        recent = conn.execute(
            "SELECT gen_params_json, last_accessed FROM cache_state "
            "WHERE last_accessed IS NOT NULL ORDER BY last_accessed DESC LIMIT 10"
        ).fetchall()
        top = conn.execute(
            "SELECT cp.cache_key, COUNT(*) AS n, cs.gen_params_json "
            "FROM cache_poems cp LEFT JOIN cache_state cs USING(cache_key) "
            "GROUP BY cp.cache_key ORDER BY n DESC, cp.cache_key LIMIT 10"
        ).fetchall()
    finally:
        conn.close()
    db_size = os.path.getsize(CACHE_DBFILE) if os.path.exists(CACHE_DBFILE) else 0
    return {
        'db_path': CACHE_DBFILE,
        'db_size_mb': db_size / (1024 * 1024),
        'max_in_flight': MAX_REGEN_IN_FLIGHT,
        'running': running,
        'total_poems': total_poems,
        'distinct_combos': distinct_combos,
        'starved': starved,
        'oldest': oldest or '-',
        'newest': newest or '-',
        'recent': recent,
        'top': top,
    }
