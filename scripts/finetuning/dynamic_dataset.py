"""
Dynamic PyTorch Dataset for poem generation with format variations.

This module provides a PyTorch Dataset that loads poems from the SQLite database
and generates formatted output on-the-fly during training.
"""

import sqlite3
import json
from collections import defaultdict
import sys
from pathlib import Path
import random
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from enum import Enum

import torch
from torch.utils.data import Dataset

# Add paths for kveta
sys.path.append(str(Path(__file__).parent / "edupo/kveta"))
sys.path.append(str(Path(__file__).parent / "edupo/scripts/diphthongs"))
from kveta import Kveta


# Constants
METRE_PRIORITY = defaultdict(int)
METRE_PRIORITY['T'] = 5
METRE_PRIORITY['J'] = 4
METRE_PRIORITY['D'] = 3
METRE_PRIORITY['A'] = 2
METRE_PRIORITY['N'] = -1


def dict_factory(cursor, row):
    """Convert SQLite row to dictionary."""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def add_rhyme_annotation(poem):
    """Add rhyme annotation to poem syllables."""
    for verse in poem:
        last_word = -1
        penultimate_word = -2
        lim = 2

        if len(verse["words"][-1]["syllables"]) == 0:
            last_word = -2
            penultimate_word = -3
            lim = 3
            print(f"WARNING: No syllables for the last word: {repr(verse['text'])}", file=sys.stderr)

        if len(verse["words"][last_word]["syllables"]) >= 2:  # multi-syllable word
            verse["words"][last_word]["syllables"][-2]["rhyme_from"] = 'v'
            verse["words"][last_word]["syllables"][-1]["rhyme_from"] = 'c'
        elif len(verse["words"]) >= lim and verse["words"][penultimate_word]["vec"] and (verse["words"][penultimate_word]["vec"]["prep"][0] == 1 or verse["words"][last_word]["vec"]["content"][0] == 0):
            verse["words"][penultimate_word]["syllables"][-1]["rhyme_from"] = 'v'
            verse["words"][last_word]["syllables"][-1]["rhyme_from"] = 'c'
        elif verse["words"][last_word]["syllables"][-1]["ph_end_consonants"]:
            verse["words"][last_word]["syllables"][-1]["rhyme_from"] = 'v'
        else:
            if verse["words"][last_word]["syllables"][-1]['ph_consonants']:
                verse["words"][last_word]["syllables"][-1]["rhyme_from"] = 'c'
            else:
                verse["words"][last_word]["syllables"][-1]["rhyme_from"] = 'v'


def get_rhyming_part(syllables):
    """Extract the rhyming part from syllables."""
    r_end = ""
    for i, syllable in enumerate(syllables):
        if syllable['rhyme_from'] == 'c':
            r_end += (syllable['ort_consonants'][-1] if i == 0 else syllable['ort_consonants']) + syllable['ort_vowels'] + syllable['ort_end_consonants']
        elif syllable['rhyme_from'] == 'v':
            r_end += syllable['ort_vowels'] + syllable['ort_end_consonants']
        elif syllable['rhyme_from'] == 'ec':
            r_end += syllable['end_consonants'][-1] if i == 0 else syllable['end_consonants']
        else:
            raise ValueError(f"Invalid rhyme_from value {syllable['rhyme_from']}")
    return r_end


def select_metre(metres):
    """Select the dominant metre from a list."""
    return max(metres, key=lambda m: METRE_PRIORITY[m])


def separate_stanzas(poem):
    """Separate poem into stanzas."""
    stanzas = []
    current_stanza = []
    stanza_num = None
    for verse in poem:
        if verse['stanza'] != stanza_num:
            if current_stanza:
                stanzas.append(current_stanza)
            current_stanza = []
            stanza_num = verse['stanza']
        current_stanza.append(verse)
    if current_stanza:
        stanzas.append(current_stanza)
    return stanzas


# Format Variation System
class AuthorFormat(Enum):
    """Author field format variations."""
    FULL = "full"  # <author>Full Name</author>
    NAME_SURNAME = "name_surname"  # <author>FirstName LastName</author>
    OMIT = "omit"  # No author tag
    GUESS = "guess"  # <guess_author/> in header, <author>...</author> after poem


class TitleFormat(Enum):
    """Title field format variations."""
    FULL = "full"  # <title>Title Text</title>
    OMIT = "omit"  # No title tag
    GUESS = "guess"  # <guess_title/> in header, <title>...</title> after poem


class YearFormat(Enum):
    """Year field format variations."""
    FULL = "full"  # <year>1836</year>
    OMIT = "omit"  # No year tag
    GUESS = "guess"  # <guess_year/> in header, <year>...</year> after poem


class MotiveFormat(Enum):
    """Motive field format variations."""
    FULL = "full"  # <motives>...</motives>
    OMIT = "omit"  # No motives tag
    GUESS = "guess"  # <guess_motives/> in header, <motives>...</motives> after poem


@dataclass
class FormatConfig:
    """Configuration for format variations."""
    author_format: AuthorFormat = AuthorFormat.FULL
    title_format: TitleFormat = TitleFormat.FULL
    year_format: YearFormat = YearFormat.FULL
    motive_format: MotiveFormat = MotiveFormat.FULL

    @classmethod
    def random_config(cls, author_weights: Optional[Dict[AuthorFormat, float]] = None,
                     title_weights: Optional[Dict[TitleFormat, float]] = None,
                     year_weights: Optional[Dict[YearFormat, float]] = None,
                     motive_weights: Optional[Dict[MotiveFormat, float]] = None):
        """Generate a random format configuration.

        Args:
            author_weights: Dictionary mapping AuthorFormat to probability weights.
                          If None, uses equal weights for all formats.
            title_weights: Dictionary mapping TitleFormat to probability weights.
                          If None, uses equal weights for all formats.
            year_weights: Dictionary mapping YearFormat to probability weights.
                          If None, uses equal weights for all formats.
            motive_weights: Dictionary mapping MotiveFormat to probability weights.
                          If None, uses equal weights for all formats.
        """
        # Select author format
        if author_weights is None:
            author_formats = list(AuthorFormat)
            author_format = random.choice(author_formats)
        else:
            author_formats = list(author_weights.keys())
            weights = list(author_weights.values())
            author_format = random.choices(author_formats, weights=weights, k=1)[0]

        # Select title format
        if title_weights is None:
            title_formats = list(TitleFormat)
            title_format = random.choice(title_formats)
        else:
            title_formats = list(title_weights.keys())
            weights = list(title_weights.values())
            title_format = random.choices(title_formats, weights=weights, k=1)[0]

        # Select year format
        if year_weights is None:
            year_formats = list(YearFormat)
            year_format = random.choice(year_formats)
        else:
            year_formats = list(year_weights.keys())
            weights = list(year_weights.values())
            year_format = random.choices(year_formats, weights=weights, k=1)[0]

        # Select motive format
        if motive_weights is None:
            motive_formats = list(MotiveFormat)
            motive_format = random.choice(motive_formats)
        else:
            motive_formats = list(motive_weights.keys())
            weights = list(motive_weights.values())
            motive_format = random.choices(motive_formats, weights=weights, k=1)[0]

        return cls(author_format=author_format, title_format=title_format,
                  year_format=year_format, motive_format=motive_format)


class FormatV3:
    """Format V3: Uses <rhyme_with> tags referencing previous verse with same rhyme.

    Features randomized metadata tag order in header and footer.
    """

    def format_version_tag(self):
        return "<format-v-3/>"

    def format_verse(self, verse, rhyming, stanza, verse_index):
        """Format a single verse in V3 format."""
        metre = select_metre([list(v)[0] for v in verse['metre']])
        syllables = len(verse['sections'])

        if rhyming and verse['rhyme'] is not None:
            # Find the reduplicant from the previous verse with matching rhyme number
            rhyme_with_text = self._get_rhyme_with(stanza, verse_index, verse['rhyme'])
        else:
            rhyme_with_text = 'NON'

        return '<metre>' + metre + '</metre><syllables>' + str(syllables) + '</syllables><rhyme_with>' + rhyme_with_text + "</rhyme_with>" + verse['text']

    def _get_rhyme_with(self, stanza, current_index, rhyme_num):
        """Find reduplicant from previous verse with same rhyme number."""
        for i in range(current_index):
            if stanza[i]['rhyme'] == rhyme_num:
                # Extract reduplicant from this verse
                syllables_with_rhyme = sum([[s for s in w['syllables'] if 'rhyme_from' in s] for w in stanza[i]['words']], [])
                return get_rhyming_part(syllables_with_rhyme).lower()
        # First occurrence of this rhyme - no previous verse to rhyme with
        return 'NON'


def poem_header(poem, formatter, format_config: FormatConfig):
    """Generate poem header with metadata.

    Args:
        poem: Poem dictionary with metadata
        formatter: Format instance (e.g., FormatV3)
        format_config: FormatConfig instance specifying variations

    Returns:
        tuple: (header_string, list of footer strings)
    """
    header = "<poem>\n"
    header += formatter.format_version_tag() + "\n"

    # Collect header tags and footer tags
    header_tags = []
    footers = []

    # Always include rhyme_schemes
    header_tags.append("<rhyme_schemes/>\n")

    # Handle author field variations
    if format_config.author_format == AuthorFormat.FULL:
        header_tags.append(f"<author>{poem['author']}</author>\n")
    elif format_config.author_format == AuthorFormat.NAME_SURNAME:
        # Convert "Surname, Firstname" to "Firstname Surname"
        if ',' in poem['author']:
            parts = poem['author'].split(',', 1)
            surname = parts[0].strip()
            firstname = parts[1].strip()
            formatted_author = f"{firstname} {surname}"
        else:
            # No comma, use as-is
            formatted_author = poem['author']
        header_tags.append(f"<author>{formatted_author}</author>\n")
    elif format_config.author_format == AuthorFormat.GUESS:
        header_tags.append("<guess_author/>\n")
        footers.append(f"<author>{poem['author']}</author>\n")
    # elif AuthorFormat.OMIT: do nothing

    # Handle title field variations
    if format_config.title_format == TitleFormat.FULL:
        header_tags.append(f"<title>{poem['title']}</title>\n")
    elif format_config.title_format == TitleFormat.GUESS:
        header_tags.append("<guess_title/>\n")
        footers.append(f"<title>{poem['title']}</title>\n")
    # elif TitleFormat.OMIT: do nothing

    # Handle year field variations
    if format_config.year_format == YearFormat.FULL:
        header_tags.append(f"<year>{poem['year']}</year>\n")
    elif format_config.year_format == YearFormat.GUESS:
        header_tags.append("<guess_year/>\n")
        footers.append(f"<year>{poem['year']}</year>\n")
    # elif YearFormat.OMIT: do nothing

    # Handle motive field variations
    if poem.get('motives') is not None and poem['motives']:
        # Parse motives if they're in JSON format
        try:
            if isinstance(poem['motives'], str):
                motives_list = json.loads(poem['motives'])
            else:
                motives_list = poem['motives']

            if motives_list:
                motives_text = '\n'.join(motives_list)
                if format_config.motive_format == MotiveFormat.FULL:
                    header_tags.append(f"<motives>\n{motives_text}\n</motives>\n")
                elif format_config.motive_format == MotiveFormat.GUESS:
                    header_tags.append("<guess_motives/>\n")
                    footers.append(f"<motives>\n{motives_text}\n</motives>\n")
                # elif MotiveFormat.OMIT: do nothing
        except (json.JSONDecodeError, TypeError):
            # If parsing fails, skip motives
            pass

    # Handle form
    if poem['schemes']['form'] is not None:
        header_tags.append(f"<form>{poem['schemes']['form']}</form>\n")

    # Randomize the order of header tags
    random.shuffle(header_tags)

    # Add randomized header tags to header
    for tag in header_tags:
        header += tag

    # Randomize the order of footer tags
    random.shuffle(footers)

    # Note: stanzas tag with count attribute will be added later
    return header, footers


def strophe_header(strophe):
    """Generate stanza header with rhyme scheme."""
    abeceda = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    scheme_numeric = [v['rhyme'] for v in strophe]
    for n in scheme_numeric:
        assert n is None or 0 < n, f"Invalid rhyme number {n}"
    renum = {}
    scheme = []
    for n in scheme_numeric:
        if n is None:
            scheme.append('x')
            continue
        if n not in renum:
            renum[n] = len(renum)
        scheme.append(abeceda[renum[n] % len(abeceda)])
    return '<new_stanza/>\n' + f'<rhyme_scheme length="{len(scheme)}">' + ' '.join(scheme) + "</rhyme_scheme>\n", len(renum) > 0


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
        db_path: Path to SQLite database (default: ../../data/db_s_motivama.db)
        max_poems: Maximum number of poems to load (None = all)
        format_version: Format version to use (default: 3 for V3)
        shuffle: Whether to randomize poem order after loading (default: True)
        random_seed: Random seed for shuffling (None = use current state)
        use_format_variations: Whether to use random format variations per poem (default: True)
        author_weights: Dictionary mapping AuthorFormat to probability weights
        title_weights: Dictionary mapping TitleFormat to probability weights
        year_weights: Dictionary mapping YearFormat to probability weights
        motive_weights: Dictionary mapping MotiveFormat to probability weights
        verse_regenerate_prob: Probability of verse regeneration mode (default: 0.1)
    """

    def __init__(self, db_path="../../data/db_s_motivama.db", max_poems=None, format_version=3,
                 shuffle=True, random_seed=None, use_format_variations=True,
                 author_weights: Optional[Dict[AuthorFormat, float]] = None,
                 title_weights: Optional[Dict[TitleFormat, float]] = None,
                 year_weights: Optional[Dict[YearFormat, float]] = None,
                 motive_weights: Optional[Dict[MotiveFormat, float]] = None,
                 verse_regenerate_prob: float = 0.1):
        self.db_path = db_path
        self.format_version = format_version
        self.formatter = FormatV3()
        self.poems = []
        self.shuffle = shuffle
        self.random_seed = random_seed
        self.use_format_variations = use_format_variations
        self.author_weights = author_weights
        self.title_weights = title_weights
        self.year_weights = year_weights
        self.motive_weights = motive_weights
        self.verse_regenerate_prob = verse_regenerate_prob

        # Load and process poems from database
        self._load_poems(max_poems)

        # Shuffle poems if requested
        if self.shuffle:
            if self.random_seed is not None:
                random.seed(self.random_seed)
            random.shuffle(self.poems)
            print(f"Shuffled {len(self.poems)} poems.", file=sys.stderr)

    def _load_poems(self, max_poems=None):
        """Load poems from SQLite database and process them."""
        print(f"Loading poems from {self.db_path}...", file=sys.stderr)

        sqlite3.register_converter("json", json.loads)
        with sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES) as db:
            db.row_factory = dict_factory
            query = "SELECT poems.id, poems.author, poems.title, body, year, poems.schemes, poems.motives FROM poems JOIN books on poems.book_id = books.id WHERE poems.duplicate IS NULL"
            if max_poems is not None:
                query += f" LIMIT {max_poems}"
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
                kv.phoebe2cft()
                kv.syllables()
                kv.line2vec()
                add_rhyme_annotation(kv.poem_)

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

        # Generate random format configuration for this poem
        if self.use_format_variations:
            format_config = FormatConfig.random_config(author_weights=self.author_weights,
                                                       title_weights=self.title_weights,
                                                       year_weights=self.year_weights,
                                                       motive_weights=self.motive_weights)
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

        # Generate formatted output with header
        header, footers = poem_header(poem, self.formatter, format_config)
        output = header

        # Add verse_regenerate tag if needed
        if do_verse_regenerate and regenerate_verse_idx is not None:
            output += '<verse_regenerate/>\n'

        # Add stanzas opening tag with length attribute
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


if __name__ == "__main__":
    # Test the dataset
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--db-path", type=str, default="../../data/db_s_motivama.db",
                        help="Path to SQLite database")
    parser.add_argument("--max-poems", type=int, default=10,
                        help="Maximum number of poems to load for testing")
    parser.add_argument("--show-poem", type=int, default=0,
                        help="Index of poem to display")
    parser.add_argument("--test-variations", action="store_true",
                        help="Test format variations by showing same poem multiple times")
    parser.add_argument("--num-variations", type=int, default=5,
                        help="Number of format variations to show (with --test-variations)")

    args = parser.parse_args()

    # Create dataset
    dataset = DynamicPoemDataset(db_path=args.db_path, max_poems=args.max_poems)

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
