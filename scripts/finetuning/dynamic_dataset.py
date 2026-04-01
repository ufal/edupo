"""
Dynamic PyTorch Dataset for poem generation with format variations.

This module provides a PyTorch Dataset that loads poems from the SQLite database
and generates formatted output on-the-fly during training.
"""

# TODO better format info at the start of the poem (prevent generating of regeneration in first generation)
# TODO better rhyme-with: rhyme from the last rhyming verse, not the first one
# TODO add option for old-style rhyme -- reduplicant for each rhyme
# TODO euroLLM: handle start and end tokens properly

from format_v3 import FormatV3

import sqlite3
import json
import sys
from pathlib import Path
import random
from typing import Optional, Dict



# Add parent directory for sibling module imports
# sys.path.append(str(Path(__file__).parent))

from format_v3 import FormatV3
from format_v4 import FormatV4
from poem_utils import dict_factory, add_rhyme_annotation, separate_stanzas, select_metre
from format_config import (
    AuthorFormat, TitleFormat, YearFormat, MotiveFormat, BookFormat,
    FormatConfig, poem_header, strophe_header,
)

from torch.utils.data import Dataset

# Add paths for kveta
sys.path.append(str(Path(__file__).parent / "edupo/kveta"))
sys.path.append(str(Path(__file__).parent / "edupo/scripts/diphthongs"))
from kveta import Kveta




class MappedDynamicDataset(Dataset):
    """
    Wrapper that applies a mapping function to a dynamic dataset on-the-fly.

    This preserves dynamic format generation by applying the mapping function
    in __getitem__ rather than preprocessing all data.
    """

    def __init__(self, base_dataset, function, batched=False, batch_size=1000,
                 remove_columns=None, num_proc=None, desc=None, **kwargs):
        self.base_dataset = base_dataset
        self.function = function
        self.batched = batched
        self.batch_size = batch_size
        self.remove_columns = remove_columns or []
        # Filter out map-specific arguments that shouldn't be passed to the function
        # num_proc, desc, batch_size are for map() itself, not the function
        self.function_kwargs = kwargs

    def __len__(self):
        return len(self.base_dataset)

    def __getitem__(self, idx):
        # Get dynamically formatted item from base dataset
        item = self.base_dataset[idx]

        # Apply the mapping function (only pass function-specific kwargs, not map kwargs)
        if self.batched:
            # Convert single item to batch format: {'text': 'poem'} -> {'text': ['poem']}
            batch = {k: [v] for k, v in item.items()}
            result = self.function(batch, **self.function_kwargs)
            # Unwrap the batch: {'input_ids': [[1,2,3]]} -> {'input_ids': [1,2,3]}
            mapped_item = {k: v[0] for k, v in result.items()}
        else:
            mapped_item = self.function(item, **self.function_kwargs)

        # Remove specified columns
        for col in self.remove_columns:
            mapped_item.pop(col, None)

        return mapped_item

    def map(self, function, *args, **kwargs):
        """Support chaining of map operations."""
        return MappedDynamicDataset(self, function, *args, **kwargs)


class DynamicPoemDataset(Dataset):
    """
    PyTorch Dataset that loads poems from SQLite database and formats them dynamically.

    Args:
        db_path: Path to SQLite database (default: data/new.db)
        max_poems: Maximum number of poems to load (None = all)
        format_version: Format version to use (default: 3 for V3)
        shuffle: Whether to randomize poem order after loading (default: True)
        random_seed: Random seed for shuffling (None = use current state)
        use_format_variations: Whether to use random format variations per poem (default: True)
        author_weights: Dictionary mapping AuthorFormat to probability weights
        title_weights: Dictionary mapping TitleFormat to probability weights
        year_weights: Dictionary mapping YearFormat to probability weights
        motive_weights: Dictionary mapping MotiveFormat to probability weights
        book_weights: Dictionary mapping BookFormat to probability weights
        verse_regenerate_prob: Probability of verse regeneration mode (default: 0.1)
    """

    def __init__(self, db_path="data/new.db", max_poems=None, start_poem=None,
                 format_version=4, shuffle=True, random_seed=None,
                 use_format_variations=True,
                 author_weights: Optional[Dict[AuthorFormat, float]] = None,
                 title_weights: Optional[Dict[TitleFormat, float]] = None,
                 year_weights: Optional[Dict[YearFormat, float]] = None,
                 motive_weights: Optional[Dict[MotiveFormat, float]] = None,
                 book_weights: Optional[Dict[BookFormat, float]] = None,
                 verse_regenerate_prob: float = 0.1):
        self.db_path = db_path
        self.start_poem = start_poem
        self.format_version = format_version
        if format_version == 4:
            self.formatter = FormatV4()
        else:
            self.formatter = FormatV3()
        self.poems = []
        self.shuffle = shuffle
        self.random_seed = random_seed
        self.use_format_variations = use_format_variations
        self.author_weights = author_weights
        self.title_weights = title_weights
        self.year_weights = year_weights
        self.motive_weights = motive_weights
        self.book_weights = book_weights
        self.verse_regenerate_prob = verse_regenerate_prob

        # Load and process poems from database
        self._load_poems(max_poems, start_poem)

        # Shuffle poems if requested
        if self.shuffle:
            if self.random_seed is not None:
                random.seed(self.random_seed)
            random.shuffle(self.poems)
            print(f"Shuffled {len(self.poems)} poems.", file=sys.stderr)

    def _load_poems(self, max_poems=None, start_poem=None):
        """Load poems from SQLite database and process them."""
        print(f"Loading poems from {self.db_path}...", file=sys.stderr)

        sqlite3.register_converter("json", json.loads)
        with sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES) as db:
            db.row_factory = dict_factory
            query = "SELECT poems.id, poems.author, poems.title, body, year, poems.schemes, poems.motives, books.title as b_title FROM poems JOIN books on poems.book_id = books.id WHERE poems.duplicate IS NULL"
            if max_poems is not None:
                query += f" LIMIT {max_poems}"
            if start_poem is not None:
                # OFFSET requires a LIMIT in SQLite; use -1 if no max_poems given
                if max_poems is None:
                    query += f" LIMIT -1"
                query += f" OFFSET {start_poem}"
            query += ";"
            poems = db.execute(query).fetchall()
            print(f"Loaded {len(poems)} poems from database.", file=sys.stderr)

        # Process each poem
        processed_count = 0
        for p in poems:
            try:
                # Process with Kveta
                kv = Kveta('')
                kv.read_ccv(p['body'])
                try:
                    kv.phoebe2cft()
                except KeyError:
                    kv.phonetics()
                kv.syllables()
                kv.line2vec()
                poem_warnings = []
                add_rhyme_annotation(kv.poem_, warnings=poem_warnings)
                for w in poem_warnings:
                    print(f"  poem {p['id']}: {w}", file=sys.stderr)

                # Separate into stanzas
                p['body'] = separate_stanzas(kv.poem_)

                # Store processed poem
                self.poems.append(p)
                processed_count += 1

                if processed_count % 1000 == 0:
                    print(f"Processed {processed_count}/{len(poems)} poems...", file=sys.stderr)

            except Exception as e:
                print(f"ERROR processing poem {p['id']} {p['author']}: {p['title']} ({p['year']})", file=sys.stderr)
                print(f"  {str(e)}", file=sys.stderr)
                continue

        print(f"Successfully processed {len(self.poems)} poems.", file=sys.stderr)

    def __len__(self):
        """Return number of poems in dataset."""
        return len(self.poems)

    def map(self, function, *args, **kwargs):
        """
        Compatibility method for HuggingFace Trainer.

        Returns a wrapper that applies the function dynamically in __getitem__.
        This preserves dynamic format generation while satisfying the trainer's expectations.
        """
        # Create a wrapper that applies the function on-the-fly
        return MappedDynamicDataset(self, function, *args, **kwargs)

    def __getitem__(self, idx):
        """
        Get a poem at the given index, formatted as a dictionary with 'text' field.

        Args:
            idx: Index of the poem

        Returns:
            Dictionary with 'text' field containing formatted poem
        """
        poem = self.poems[idx]

        try:
            # Generate random format configuration for this poem
            if self.use_format_variations:
                format_config = FormatConfig.random_config(author_weights=self.author_weights,
                                                           title_weights=self.title_weights,
                                                           year_weights=self.year_weights,
                                                           motive_weights=self.motive_weights,
                                                           book_weights=self.book_weights)
            else:
                # Use default configuration (all FULL formats)
                format_config = FormatConfig()

            # Determine if we should do verse regeneration
            do_verse_regenerate = random.random() < self.verse_regenerate_prob
            regenerate_verse_idx = None
            regenerated_text = None

            if do_verse_regenerate:
                # Count total verses in the poem
                total_verses = sum(len(stanza) for stanza in poem['body'])
                if total_verses > 0:
                    # Select a random verse to regenerate
                    regenerate_verse_idx = random.randint(0, total_verses - 1)

            # Delegate to formatter if it handles full poem formatting (V4+)
            if hasattr(self.formatter, 'format_poem'):
                output = self.formatter.format_poem(poem, format_config, regenerate_verse_idx)
                return {'text': output}

            # V3 formatting: build output from header, stanzas, footer
            header, footers = poem_header(poem, self.formatter, format_config)
            output = header

            # Add verse_regenerate tag if needed
            if do_verse_regenerate and regenerate_verse_idx is not None:
                output += '<verse_regenerate/>\n'
            else:
                output += '<no_verse_regenerate/>\n'

            # Add stanzas opening tag with length attribute
            # TODO randomize whether to include length attribute or not
            output += f'<stanzas length="{len(poem["body"])}">\n'

            # Track verse index across all stanzas
            global_verse_idx = 0

            for stanza_idx, stanza in enumerate(poem['body']):
                if stanza_idx > 0:
                    output += '\n'
                s_header, rhyming = strophe_header(stanza)
                output += s_header

                # Format each verse in the stanza
                verse_lines = []
                for verse_idx, verse in enumerate(stanza):
                    if do_verse_regenerate and global_verse_idx == regenerate_verse_idx:
                        # This is the verse to regenerate - keep metadata but replace text with <regenerate/> tag
                        metre = select_metre([list(v)[0] for v in verse['metre']])
                        syllables = len(verse['sections'])

                        if rhyming and verse['rhyme'] is not None:
                            # Find the reduplicant from the previous verse with matching rhyme number
                            rhyme_with_text = self.formatter._get_rhyme_with(stanza, verse_idx, verse['rhyme'])
                        else:
                            rhyme_with_text = 'NON'

                        verse_with_metadata = '<metre>' + metre + '</metre><syllables>' + str(syllables) + '</syllables><rhyme_with>' + rhyme_with_text + "</rhyme_with><regenerate/>"
                        verse_lines.append(verse_with_metadata)
                        # Save just the verse text (not the metadata tags) for the footer
                        regenerated_text = verse['text']
                    else:
                        # Normal verse formatting
                        verse_lines.append(self.formatter.format_verse(verse, rhyming, stanza, verse_idx))
                    global_verse_idx += 1

                output += '\n'.join(verse_lines)

            # Close stanzas tag
            output += '\n</stanzas>\n'

            # Add regenerated verse text if applicable
            if do_verse_regenerate and regenerated_text is not None:
                output += f'<regenerated>{regenerated_text}</regenerated>\n'

            # Add footers (already randomized)
            for footer in footers:
                output += footer

            output += '</poem>'

            return {'text': output}

        except Exception as e:
            print(f"ERROR formatting poem {poem['id']}: {e}", file=sys.stderr)
            return {'text': ''}


if __name__ == "__main__":
    # Test the dataset
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--db-path", type=str, default="data/new.db",
                        help="Path to SQLite database")
    parser.add_argument("--max-poems", type=int, default=None,
                        help="Maximum number of poems to load (default: 10 for normal mode, all for --dry-run)")
    parser.add_argument("--start-poem", type=int, default=None,
                        help="Start loading from the Nth poem in the database (0-based offset)")
    parser.add_argument("--show-poem", type=int, default=0,
                        help="Index of poem to display")
    parser.add_argument("--test-variations", action="store_true",
                        help="Test format variations by showing same poem multiple times")
    parser.add_argument("--num-variations", type=int, default=5,
                        help="Number of format variations to show (with --test-variations)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Load and process all poems, listing all warnings and errors "
                             "(with poem ID) without building a usable dataset")

    args = parser.parse_args()

    if args.dry_run:
        from poem_utils import get_rhyming_part

        dataset = DynamicPoemDataset(
            db_path=args.db_path,
            max_poems=args.max_poems,
            start_poem=args.start_poem,
            shuffle=False,
        )

        print(f"\nDry run: {len(dataset)} poems loaded successfully.", file=sys.stderr)

        # Try to extract rhyming parts for every verse (catches get_rhyming_part errors)
        rhyme_errors = 0
        for poem in dataset.poems:
            for stanza in poem['body']:
                for verse in stanza:
                    try:
                        syllables_with_rhyme = sum(
                            [[s for s in w['syllables'] if 'rhyme_from' in s]
                             for w in verse['words']], []
                        )
                        get_rhyming_part(syllables_with_rhyme)
                    except Exception as e:
                        print(
                            f"  poem {poem['id']}: ERROR extracting rhyme "
                            f"for verse {repr(verse['text'])}: {e}",
                            file=sys.stderr,
                        )
                        rhyme_errors += 1

        print(f"Dry run complete. Rhyme extraction errors: {rhyme_errors}.", file=sys.stderr)

    else:
        # Normal mode: default to 10 poems when --max-poems not given
        max_poems = args.max_poems if args.max_poems is not None else 10

        # Create dataset
        dataset = DynamicPoemDataset(db_path=args.db_path, max_poems=max_poems,
                                     start_poem=args.start_poem)

        print(f"\nDataset contains {len(dataset)} poems.\n")

        if args.test_variations:
            # Show the same poem with different format variations
            print(f"Testing format variations for poem at index {args.show_poem}:")
            print("=" * 80)
            for i in range(args.num_variations):
                print(f"\nVariation {i+1}:")
                print("-" * 80)
                print(dataset[args.show_poem]['text'])
                print("-" * 80)
        else:
            # Show a sample poem
            if args.show_poem < len(dataset):
                print(f"Sample poem (index {args.show_poem}):")
                print("=" * 80)
                print(dataset[args.show_poem]['text'])
                print("=" * 80)
