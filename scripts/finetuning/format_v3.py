"""
Format V3: Uses <rhyme_with> tags referencing previous verse with same rhyme.

Features randomized metadata tag order in header and footer.
"""

from poem_utils import select_metre, get_rhyming_part


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
