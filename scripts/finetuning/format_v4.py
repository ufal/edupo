"""
Format V4: JSON-based format for poem generation.

Same information as V3 but uses JSON structure instead of XML tags.
Metadata key order is randomized (like V3's randomized tag order).

Example output:
{"format": "v4", "syllables_format": "before", "metre_format": "before", "rhyme_format": "before", "rhyme_schemes": true, "author": "Mácha, Karel Hynek", "year": 1836,
"title": "Máj", "form": "sonnet", "verse_regenerate": false, "stanzas_count": 2,
"stanzas": [
{"rhyme_scheme": "A B A B", "verses": [
{"metre": "T", "syllables": 8, "rhyme_with": null, "text": "Byl pozdní večer – první máj –"},
{"metre": "T", "syllables": 8, "rhyme_with": null, "text": "večerní máj – byl lásky čas."},
{"metre": "T", "syllables": 8, "rhyme_with": "máj", "text": "Hrdliččin zval ku lásce hlas,"},
{"metre": "T", "syllables": 8, "rhyme_with": "čas", "text": "kde borový zaváněl háj."}]}]}
"""

import json
import random

from poem_utils import select_metre, get_rhyming_part
from format_config import (
    AuthorFormat, TitleFormat, YearFormat, MotiveFormat, BookFormat,
    FormatConfig,
)


class FormatV4:
    """Format V4: JSON-based format.

    Provides format_poem() which handles the entire poem formatting,
    since JSON structure differs fundamentally from V3's XML tags.
    """

    def format_poem(self, poem, format_config, regenerate_verse_idx=None):
        """Format the entire poem as a JSON string.

        Args:
            poem: Poem dict with metadata and body (list of stanzas)
            format_config: FormatConfig instance
            regenerate_verse_idx: Global verse index to regenerate (None = no regeneration)

        Returns:
            Formatted poem as a JSON string
        """
        meta_entries = []
        footer_entries = []

        meta_entries.append('"rhyme_schemes": true')

        # Author
        if format_config.author_format == AuthorFormat.FULL:
            meta_entries.append(f'"author": {json.dumps(poem["author"], ensure_ascii=False)}')
        elif format_config.author_format == AuthorFormat.NAME_SURNAME:
            if ',' in poem['author']:
                parts = poem['author'].split(',', 1)
                formatted_author = f"{parts[1].strip()} {parts[0].strip()}"
            else:
                formatted_author = poem['author']
            meta_entries.append(f'"author": {json.dumps(formatted_author, ensure_ascii=False)}')
        elif format_config.author_format == AuthorFormat.PREDICT:
            meta_entries.append('"author": null')
            footer_entries.append(f'"author_answer": {json.dumps(poem["author"], ensure_ascii=False)}')

        # Title
        if format_config.title_format == TitleFormat.FULL:
            meta_entries.append(f'"title": {json.dumps(poem["title"], ensure_ascii=False)}')
        elif format_config.title_format == TitleFormat.PREDICT:
            meta_entries.append('"title": null')
            footer_entries.append(f'"title_answer": {json.dumps(poem["title"], ensure_ascii=False)}')

        # Year
        if format_config.year_format == YearFormat.FULL:
            meta_entries.append(f'"year": {json.dumps(poem["year"])}')
        elif format_config.year_format == YearFormat.PREDICT:
            meta_entries.append('"year": null')
            footer_entries.append(f'"year_answer": {json.dumps(poem["year"])}')

        # Motives
        if poem.get('motives') is not None and poem['motives']:
            try:
                motives_list = json.loads(poem['motives']) if isinstance(poem['motives'], str) else poem['motives']
                if motives_list:
                    if format_config.motive_format == MotiveFormat.FULL:
                        meta_entries.append(f'"motives": {json.dumps(motives_list, ensure_ascii=False)}')
                    elif format_config.motive_format == MotiveFormat.PREDICT:
                        meta_entries.append('"motives": null')
                        footer_entries.append(f'"motives_answer": {json.dumps(motives_list, ensure_ascii=False)}')
            except (json.JSONDecodeError, TypeError):
                pass

        # Book title
        if poem.get('b_title') is not None and poem['b_title']:
            if format_config.book_format == BookFormat.FULL:
                meta_entries.append(f'"book_title": {json.dumps(poem["b_title"], ensure_ascii=False)}')
            elif format_config.book_format == BookFormat.PREDICT:
                meta_entries.append('"book_title": null')
                footer_entries.append(f'"book_title_answer": {json.dumps(poem["b_title"], ensure_ascii=False)}')

        # Form
        if poem['schemes'] is not None and poem['schemes']['form'] is not None:
            meta_entries.append(f'"form": {json.dumps(poem["schemes"]["form"], ensure_ascii=False)}')

        # Randomize metadata and footer order
        random.shuffle(meta_entries)
        random.shuffle(footer_entries)

        # Build output: format key is always first
        syllables_format_choice = random.choice(["before", "after", "none"])
        metre_format_choice = random.choice(["before", "after", "none"])
        rhyme_format_choice = random.choice(["before", "none"])
        
        parts = [
            '"format": "v4"',
            f'"syllables_format": "{syllables_format_choice}"',
            f'"metre_format": "{metre_format_choice}"',
            f'"rhyme_format": "{rhyme_format_choice}"'
        ]
        parts.extend(meta_entries)

        do_regenerate = regenerate_verse_idx is not None
        parts.append(f'"verse_regenerate": {"true" if do_regenerate else "false"}')
        parts.append(f'"stanzas_count": {len(poem["body"])}')

        output = '{' + ', '.join(parts) + ',\n"stanzas": [\n'

        # Format stanzas
        global_verse_idx = 0
        regenerated_text = None

        for stanza_idx, stanza in enumerate(poem['body']):
            if stanza_idx > 0:
                output += ',\n'

            rhyme_scheme, rhyming = self._compute_rhyme_scheme(stanza)
            output += '{"rhyme_scheme": ' + json.dumps(rhyme_scheme) + ', "verses": [\n'

            verse_lines = []
            for verse_idx, verse in enumerate(stanza):
                metre = select_metre([list(v)[0] for v in verse['metre']])
                syllables = len(verse['sections'])

                if rhyming and verse['rhyme'] is not None:
                    rhyme_with = self._get_rhyme_with(stanza, verse_idx, verse['rhyme'])
                else:
                    rhyme_with = None

                rw_json = json.dumps(rhyme_with, ensure_ascii=False)

                if do_regenerate and global_verse_idx == regenerate_verse_idx:
                    text_json = "null"
                    regenerated_text = verse['text']
                else:
                    text_json = json.dumps(verse['text'], ensure_ascii=False)

                verse_parts = []
                
                # 'before' parts
                if metre_format_choice == "before":
                    verse_parts.append(f'"metre": "{metre}"')
                if syllables_format_choice == "before":
                    verse_parts.append(f'"syllables": {syllables}')
                if rhyme_format_choice == "before":
                    verse_parts.append(f'"rhyme_with": {rw_json}')
                    
                # text
                verse_parts.append(f'"text": {text_json}')
                
                # 'after' parts
                if metre_format_choice == "after":
                    verse_parts.append(f'"metre": "{metre}"')
                if syllables_format_choice == "after":
                    verse_parts.append(f'"syllables": {syllables}')

                verse_line = "{" + ", ".join(verse_parts) + "}"

                verse_lines.append(verse_line)
                global_verse_idx += 1

            output += ',\n'.join(verse_lines)
            output += '\n]}'

        output += '\n]'

        # Regenerated text
        if do_regenerate and regenerated_text is not None:
            output += f',\n"regenerated": {json.dumps(regenerated_text, ensure_ascii=False)}'

        # Footer entries (guessed answers)
        for entry in footer_entries:
            output += ',\n' + entry

        output += '}'

        return output

    def _get_rhyme_with(self, stanza, current_index, rhyme_num):
        """Find reduplicant from previous verse with same rhyme number."""
        for i in range(current_index):
            if stanza[i]['rhyme'] == rhyme_num:
                syllables_with_rhyme = sum(
                    [[s for s in w['syllables'] if 'rhyme_from' in s] for w in stanza[i]['words']], []
                )
                return get_rhyming_part(syllables_with_rhyme).lower()
        return None

    def _compute_rhyme_scheme(self, strophe):
        """Compute rhyme scheme string and whether stanza has rhyming."""
        abeceda = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        scheme_numeric = [v['rhyme'] for v in strophe]
        renum = {}
        scheme = []
        for n in scheme_numeric:
            if n is None:
                scheme.append('x')
                continue
            if n not in renum:
                renum[n] = len(renum)
            scheme.append(abeceda[renum[n] % len(abeceda)])
        return ' '.join(scheme), len(renum) > 0
