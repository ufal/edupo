"""
Format configuration and shared formatting infrastructure.

Defines format variation enums, FormatConfig dataclass, and shared
header/strophe formatting used across all format versions.
"""

import json
import random
from dataclasses import dataclass
from typing import Optional, Dict
from enum import Enum


# Format Variation System
class AuthorFormat(Enum):
    """Author field format variations."""
    FULL = "full"  # <author>Full Name</author>
    NAME_SURNAME = "name_surname"  # <author>FirstName LastName</author>
    OMIT = "omit"  # No author tag
    PREDICT = "predict"  # <guess_author/> in header, <author>...</author> after poem


class TitleFormat(Enum):
    """Title field format variations."""
    FULL = "full"  # <title>Title Text</title>
    OMIT = "omit"  # No title tag
    PREDICT = "predict"  # <guess_title/> in header, <title>...</title> after poem


class YearFormat(Enum):
    """Year field format variations."""
    FULL = "full"  # <year>1836</year>
    OMIT = "omit"  # No year tag
    PREDICT = "predict"  # <guess_year/> in header, <year>...</year> after poem


class MotiveFormat(Enum):
    """Motive field format variations."""
    FULL = "full"  # <motives>...</motives>
    OMIT = "omit"  # No motives tag
    PREDICT = "predict"  # <guess_motives/> in header, <motives>...</motives> after poem


class BookFormat(Enum):
    """Book title field format variations."""
    FULL = "full"  # <book_title>Title Text</book_title>
    OMIT = "omit"  # No book_title tag
    PREDICT = "predict"  # <guess_book_title/> in header, <book_title>...</book_title> after poem


@dataclass
class FormatConfig:
    """Configuration for format variations."""
    author_format: AuthorFormat = AuthorFormat.FULL
    title_format: TitleFormat = TitleFormat.FULL
    year_format: YearFormat = YearFormat.FULL
    motive_format: MotiveFormat = MotiveFormat.FULL
    book_format: BookFormat = BookFormat.FULL

    @classmethod
    def random_config(cls, author_weights: Optional[Dict[AuthorFormat, float]] = None,
                     title_weights: Optional[Dict[TitleFormat, float]] = None,
                     year_weights: Optional[Dict[YearFormat, float]] = None,
                     motive_weights: Optional[Dict[MotiveFormat, float]] = None,
                     book_weights: Optional[Dict[BookFormat, float]] = None):
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
            book_weights: Dictionary mapping BookFormat to probability weights.
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

        # Select book format
        if book_weights is None:
            book_formats = list(BookFormat)
            book_format = random.choice(book_formats)
        else:
            book_formats = list(book_weights.keys())
            weights = list(book_weights.values())
            book_format = random.choices(book_formats, weights=weights, k=1)[0]

        return cls(author_format=author_format, title_format=title_format,
                  year_format=year_format, motive_format=motive_format,
                  book_format=book_format)


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
    elif format_config.author_format == AuthorFormat.PREDICT:
        header_tags.append("<guess_author/>\n")
        footers.append(f"<author>{poem['author']}</author>\n")
    # elif AuthorFormat.OMIT: do nothing

    # Handle title field variations
    if format_config.title_format == TitleFormat.FULL:
        header_tags.append(f"<title>{poem['title']}</title>\n")
    elif format_config.title_format == TitleFormat.PREDICT:
        header_tags.append("<guess_title/>\n")
        footers.append(f"<title>{poem['title']}</title>\n")
    # elif TitleFormat.OMIT: do nothing

    # Handle year field variations
    if format_config.year_format == YearFormat.FULL:
        header_tags.append(f"<year>{poem['year']}</year>\n")
    elif format_config.year_format == YearFormat.PREDICT:
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
                elif format_config.motive_format == MotiveFormat.PREDICT:
                    header_tags.append("<guess_motives/>\n")
                    footers.append(f"<motives>\n{motives_text}\n</motives>\n")
                # elif MotiveFormat.OMIT: do nothing
        except (json.JSONDecodeError, TypeError):
            # If parsing fails, skip motives
            pass

    # Handle book title field variations
    if poem.get('b_title') is not None and poem['b_title']:
        if format_config.book_format == BookFormat.FULL:
            header_tags.append(f"<book_title>{poem['b_title']}</book_title>\n")
        elif format_config.book_format == BookFormat.PREDICT:
            header_tags.append("<guess_book_title/>\n")
            footers.append(f"<book_title>{poem['b_title']}</book_title>\n")
        # elif BookFormat.OMIT: do nothing

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
