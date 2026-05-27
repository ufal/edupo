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
from datetime import datetime

logger = logging.getLogger(__name__)

CACHE_DBFILE = os.getenv('EDUPO_CACHE_DB', '/net/projects/EduPo/data/cache.db')

# A regeneration slot is considered stale (and may be reclaimed) after this many
# seconds. Must be comfortably above gunicorn's --timeout (180s) so a worker that was
# killed/recycled mid-generation does not strand the flag forever.
GENERATING_STALE_SECONDS = 300

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
    generating_since TEXT
);
CREATE TABLE IF NOT EXISTS cache_poems (
    seq        INTEGER PRIMARY KEY AUTOINCREMENT,
    cache_key  TEXT NOT NULL,
    poemid     TEXT NOT NULL,
    poem_json  TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_cache_poems_key ON cache_poems(cache_key, seq);
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
    None, also upsert cache_state with the given next_index (used on a cache miss to
    initialize the state). gen_params_json holds the FULL params dict so the background
    regen has everything it needs (modelspec, max_tries, min_meaning, max_unk, ...)."""
    poem_json = json.dumps(data, ensure_ascii=False)
    poemid = data.get('id', '')
    conn = _connect()
    try:
        conn.execute("BEGIN IMMEDIATE")
        conn.execute(
            "INSERT INTO cache_poems(cache_key, poemid, poem_json) VALUES (?,?,?)",
            (key, poemid, poem_json))
        if set_next_index_to is not None:
            conn.execute(
                "INSERT INTO cache_state(cache_key, gen_params_json, next_index, generating, generating_since) "
                "VALUES (?,?,?,0,NULL) "
                "ON CONFLICT(cache_key) DO UPDATE SET "
                "  gen_params_json=excluded.gen_params_json, next_index=excluded.next_index",
                (key, json.dumps(params, ensure_ascii=False), set_next_index_to))
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


def _bg_regen(key, params, generate_fn):
    """Background daemon-thread body: generate a fresh poem and append it to the pool.
    Always clears the `generating` flag, even on failure (e.g. OpenRouter down), so the
    key is not stranded."""
    try:
        data = generate_fn(params)  # generates + assigns id (no poemfile for cached frontends)
        _store_generated(key, params, data)
        logger.info("Background regen stored poem %s for cache_key=%s", data.get('id'), key)
    except Exception:
        logger.exception("Background poem regen failed for cache_key=%s", key)
    finally:
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

        claim = (not generating) or _is_stale(gsince, now)
        new_next = idx + 1
        new_generating = 1 if claim else generating
        new_since = now.isoformat() if claim else gsince

        if row:
            conn.execute(
                "UPDATE cache_state SET next_index=?, generating=?, generating_since=? WHERE cache_key=?",
                (new_next, new_generating, new_since, key))
        else:
            # Poems exist but no state row yet (e.g. warm-up import only populated
            # cache_poems): create the state row using the current request's params.
            conn.execute(
                "INSERT INTO cache_state(cache_key, gen_params_json, next_index, generating, generating_since) "
                "VALUES (?,?,?,?,?)",
                (key, json.dumps(params, ensure_ascii=False), new_next, new_generating, new_since))
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
