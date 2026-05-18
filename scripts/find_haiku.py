#!/usr/bin/env python3
"""
Find poems with 3 verses and syllable pattern 5-7-5 (haiku-like).

Usage:
  python find_haiku.py                    # Show count and stats by author
  python find_haiku.py --verbose          # Show author, title, and poem text
  python find_haiku.py --db-path new.db   # Specify database path
  python find_haiku.py --extended         # Find poems with repeating 5-7-5 pattern
"""

import argparse
import sqlite3
import json
import sys
from collections import Counter
from tqdm import tqdm


def dict_factory(cursor, row):
    """Convert SQLite row to dictionary."""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_syllable_counts(body):
    """Get list of syllable counts for each verse."""
    if not body:
        return None

    syllable_counts = []
    for verse in body:
        sections = verse.get('sections', '')
        if not sections:
            return None
        syllable_counts.append(len(sections))
    return syllable_counts


def is_haiku(body):
    """Check if poem has 3 verses with syllable pattern 5-7-5."""
    syllable_counts = get_syllable_counts(body)
    if syllable_counts is None or len(syllable_counts) != 3:
        return False
    return syllable_counts == [5, 7, 5]


def is_extended_haiku(body):
    """Check if poem has repeating 5-7-5 syllable pattern (at least 2 repetitions)."""
    syllable_counts = get_syllable_counts(body)
    if syllable_counts is None:
        return False

    # Must have at least 6 verses (2 repetitions of 5-7-5)
    # and the number of verses must be divisible by 3
    if len(syllable_counts) < 6 or len(syllable_counts) % 3 != 0:
        return False

    # Check that each group of 3 verses follows 5-7-5 pattern
    pattern = [5, 7, 5]
    for i in range(0, len(syllable_counts), 3):
        if syllable_counts[i:i+3] != pattern:
            return False

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Find poems with 3 verses and syllable pattern 5-7-5"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Output author, title, and poem text"
    )
    parser.add_argument(
        "--db-path",
        type=str,
        default="/net/projects/EduPo/tomas/new.db",
        help="Path to SQLite database (default: /net/projects/EduPo/data/new.db)"
    )
    parser.add_argument(
        "--extended", "-e",
        action="store_true",
        help="Find poems with repeating 5-7-5 pattern (at least 2 repetitions)"
    )
    args = parser.parse_args()

    # Connect to database
    print(f"Connecting to database: {args.db_path}", file=sys.stderr)
    sqlite3.register_converter("json", json.loads)
    try:
        with sqlite3.connect(args.db_path, detect_types=sqlite3.PARSE_DECLTYPES) as db:
            db.row_factory = dict_factory

            # Query all non-duplicate poems
            print("Fetching poems from database...", file=sys.stderr)
            query = """
                SELECT id, author, author_name, title, body
                FROM poems
                WHERE duplicate IS NULL
            """
            poems = db.execute(query).fetchall()
            print(f"Loaded {len(poems)} poems", file=sys.stderr)
    except sqlite3.OperationalError as e:
        print(f"Error connecting to database '{args.db_path}': {e}", file=sys.stderr)
        sys.exit(1)

    # Find haiku poems
    check_fn = is_extended_haiku if args.extended else is_haiku
    desc = "Scanning for extended haiku" if args.extended else "Scanning poems"
    haiku_poems = []
    for poem in tqdm(poems, desc=desc, file=sys.stderr):
        if check_fn(poem['body']):
            haiku_poems.append(poem)

    # Output results
    if args.verbose:
        for poem in haiku_poems:
            author = poem['author_name'] or poem['author'] or "Unknown"
            title = poem['title'] or "(bez názvu)"
            stanza_info = ""
            if args.extended:
                num_stanzas = len(poem['body']) // 3
                stanza_info = f" [{num_stanzas}x 5-7-5]"
            print(f"\n{author}: {title}{stanza_info}")
            print("-" * 60)
            for verse in poem['body']:
                print(verse.get('text', ''))
        print()

    # Always print summary
    poem_type = "extended haiku" if args.extended else "haiku"
    print(f"Total {poem_type} poems found: {len(haiku_poems)}")
    print()

    # Count by author
    author_counts = Counter(
        p['author_name'] or p['author'] or "Unknown"
        for p in haiku_poems
    )

    print("By author:")
    for author, count in author_counts.most_common():
        print(f"  {count:4d}  {author}")


if __name__ == "__main__":
    main()
