#!/usr/bin/env python3
# coding: utf-8
"""
Import pre-generated poems for the cached "lite" (hravá appka) frontend into the poem
cache database (see poem_cache.py).

The poems are produced sequentially into a directory of JSON files (one full poem dict
each, as produced by the backend, including a `geninput` block with the generation
parameters). This script is meant to be run repeatedly as more files appear: poems that
are already in the cache (matched by their globally-unique poem id) are skipped, so each
run only imports the new ones.

Each poem is keyed by poem_cache.cache_key_for(geninput) -- the SAME derivation the live
/gen path uses -- so an imported poem is served instantly the next time the lite frontend
requests that exact parameter combination.

Usage:
    python import_pregenerated.py [SRC_DIR] [--poemfiles] [--dry-run]

    SRC_DIR       directory of *.json poems (default: the predgenerovane path below)
    --poemfiles   ALSO write each poem to static/poemfiles/{id}.json so /show and share
                  links resolve. Off by default: these poems would otherwise show up in
                  the public /showlistgen gallery.
    --dry-run     report what would happen without writing anything

Honors the EDUPO_CACHE_DB environment variable (same as poem_cache / app.py).
"""

import argparse
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import poem_cache

DEFAULT_SRC = '/net/projects/EduPo/data/predgenerovane_pro_hravou_appku'
POEMFILES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'poemfiles')


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('src_dir', nargs='?', default=DEFAULT_SRC,
                    help=f'directory of pre-generated *.json poems (default: {DEFAULT_SRC})')
    ap.add_argument('--poemfiles', action='store_true',
                    help='also write each poem to static/poemfiles/{id}.json (for /show & share links)')
    ap.add_argument('--dry-run', action='store_true',
                    help='do not write anything, just report')
    args = ap.parse_args()

    files = sorted(glob.glob(os.path.join(args.src_dir, '*.json')))
    print(f"Source dir : {args.src_dir}")
    print(f"Cache DB   : {poem_cache.CACHE_DBFILE}")
    print(f"Poemfiles  : {'WRITE -> ' + POEMFILES_DIR if args.poemfiles else 'skip'}")
    print(f"Mode       : {'DRY RUN (no writes)' if args.dry_run else 'import'}")
    print(f"Found {len(files)} JSON file(s)\n")
    if not files:
        return

    poem_cache.init_cache_db()

    # Existing poem ids (poem ids are globally unique) -> idempotent re-runs.
    conn = poem_cache._connect()
    try:
        existing_ids = {r[0] for r in conn.execute("SELECT poemid FROM cache_poems")}
    finally:
        conn.close()

    rows = []           # (cache_key, poemid, poem_json, data) queued for insert
    seen_ids = set()
    skipped = errors = 0
    new_keys = set()

    for path in files:
        name = os.path.basename(path)
        try:
            with open(path, encoding='utf-8') as fh:
                data = json.load(fh)
        except Exception as e:
            print(f"  ERROR  {name}: cannot read ({e})")
            errors += 1
            continue

        geninput = data.get('geninput')
        poemid = data.get('id')
        if not geninput or not poemid or 'plaintext' not in data:
            print(f"  SKIP   {name}: missing geninput/id/plaintext")
            errors += 1
            continue

        if poemid in existing_ids or poemid in seen_ids:
            skipped += 1
            continue
        seen_ids.add(poemid)

        try:
            key = poem_cache.cache_key_for(geninput)
        except Exception as e:
            print(f"  ERROR  {name}: cache_key_for failed ({e})")
            errors += 1
            continue

        new_keys.add(key)
        rows.append((key, poemid, json.dumps(data, ensure_ascii=False), data))

    print(f"To import: {len(rows)}   Already present: {skipped}   Errors/skipped: {errors}")

    if args.dry_run:
        print(f"[dry-run] would add {len(new_keys)} new parameter combination(s); nothing written.")
        return

    # --- write to the cache DB (one short transaction) ---
    if rows:
        conn = poem_cache._connect()
        try:
            conn.execute("BEGIN IMMEDIATE")
            conn.executemany(
                "INSERT INTO cache_poems(cache_key, poemid, poem_json) VALUES (?,?,?)",
                [(k, pid, pj) for (k, pid, pj, _d) in rows])
            conn.execute("COMMIT")
        except Exception:
            try:
                conn.execute("ROLLBACK")
            except Exception:
                pass
            raise
        finally:
            conn.close()

    # --- optionally also write poemfiles (for /show & share links) ---
    poemfiles_written = 0
    if args.poemfiles and rows:
        os.makedirs(POEMFILES_DIR, exist_ok=True)
        for (_k, poemid, _pj, data) in rows:
            dest = os.path.join(POEMFILES_DIR, f"{poemid}.json")
            if os.path.exists(dest):
                continue
            with open(dest, 'w', encoding='utf-8') as out:
                json.dump(data, out, ensure_ascii=False, indent=4)
            poemfiles_written += 1

    # --- report ---
    conn = poem_cache._connect()
    try:
        total = conn.execute("SELECT COUNT(*) FROM cache_poems").fetchone()[0]
        distinct = conn.execute("SELECT COUNT(DISTINCT cache_key) FROM cache_poems").fetchone()[0]
    finally:
        conn.close()

    print(f"\nImported {len(rows)} poem(s); {len(new_keys)} new combination(s).")
    if args.poemfiles:
        print(f"Wrote {poemfiles_written} poemfile(s) to {POEMFILES_DIR}")
    print(f"Cache now holds {total} poem(s) across {distinct} distinct parameter combination(s).")


if __name__ == '__main__':
    main()
