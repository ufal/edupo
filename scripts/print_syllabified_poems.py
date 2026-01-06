#!/usr/bin/env python3
"""
Script to read first N poems from the database and print verses with syllables divided by '|'.

Usage:
  python print_syllabified_poems.py 10          # Print first 10 poems
  python print_syllabified_poems.py 5 --db-path new.db  # Specify database path
"""

import argparse
import sqlite3
import json
import sys
from pathlib import Path
from tqdm import tqdm

# Add paths for kveta
sys.path.append(str(Path(__file__).parent / "edupo/kveta"))
sys.path.append(str(Path(__file__).parent / "edupo/scripts/diphthongs"))
from kveta import Kveta


def dict_factory(cursor, row):
    """Convert SQLite row to dictionary."""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def syllable_to_text(syllable):
    """Convert a syllable dictionary to text representation.

    Underscores in ort_consonants represent spaces (from non-syllabic words like prepositions).
    """
    # Concatenate consonants, vowels, and end consonants
    # Replace underscores with spaces as per Kveta's convention
    text = (syllable.get('ort_consonants', '') +
            syllable.get('ort_vowels', '') +
            syllable.get('ort_end_consonants', ''))
    return text.replace('_', ' ')


def word_to_syllabified_text(word):
    """Convert a word with syllables to text with '|' separators."""
    syllables = word.get('syllables', [])
    if not syllables:
        # If no syllables, return the original word text if available
        return word.get('text', '')

    syllable_texts = [syllable_to_text(syl) for syl in syllables]
    return '|'.join(syllable_texts)


def verse_to_syllabified_text(verse):
    """Convert a verse to text with syllables divided by '|', reconstructed from syllable data."""
    words = verse.get('words', [])
    if not words:
        # Fallback to original text
        return verse.get('text', '')

    # Process each word separately to preserve word boundaries
    syllabified_words = []
    for word in words:
        syllables = word.get('syllables', [])
        if syllables:
            # Reconstruct syllables and join with '|'
            word_syllables = [syllable_to_text(syl) + '|' for syl in syllables]
            syllabified_words.append(''.join(word_syllables))
        else:
            # If word has no syllables, add the word text itself with '|'
            word_text = word.get('text', '')
            if word_text:
                syllabified_words.append(word_text + '|')

    # Join words with spaces
    return ' '.join(syllabified_words)


def main(n_poems, db_path="../../data/db_s_motivama.db"):
    """Read first N poems and print verses with syllables divided by '|'."""

    # Connect to database
    sqlite3.register_converter("json", json.loads)
    try:
        with sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES) as db:
            db.row_factory = dict_factory

            # Query first N poems
            query = """
                SELECT poems.id, poems.author, poems.title, body, year
                FROM poems
                JOIN books ON poems.book_id = books.id
                WHERE poems.duplicate IS NULL
                LIMIT ?
            """
            poems = db.execute(query, (n_poems,)).fetchall()
    except sqlite3.OperationalError as e:
        print(f"Error connecting to database '{db_path}': {e}", file=sys.stderr)
        print("Try specifying the database path with --db-path", file=sys.stderr)
        sys.exit(1)

    # Process each poem
    for poem_idx, p in enumerate(tqdm(poems, desc="Processing poems", file=sys.stderr), 1):
        try:
            # Process with Kveta to get syllables
            kv = Kveta('')
            kv.read_ccv(p['body'])
            kv.phoebe2cft()
            kv.syllables()

            # Print header
            print(f"\n{p['author']}: {p['title']} ({p['year']})")
            print("-" * 80)

            # Process each verse
            for verse in kv.poem_:
                syllabified = verse_to_syllabified_text(verse)
                print(syllabified)

            print()  # Empty line after poem

        except Exception as e:
            print(f"ERROR processing poem {p['id']}: {e}", file=sys.stderr)
            continue


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Read first N poems from database and print verses with syllables divided by '|'"
    )
    parser.add_argument(
        "n_poems",
        type=int,
        help="Number of poems to read from database"
    )
    parser.add_argument(
        "--db-path",
        type=str,
        default="../../data/db_s_motivama.db",
        help="Path to SQLite database (default: ../../data/db_s_motivama.db)"
    )

    args = parser.parse_args()

    if args.n_poems <= 0:
        print("Error: n_poems must be greater than 0", file=sys.stderr)
        sys.exit(1)

    main(args.n_poems, args.db_path)
