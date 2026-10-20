"""Keep diagnostic URLs in Gunicorn access logs without query passwords."""
import re
from urllib.parse import unquote_plus

from gunicorn.glogging import Logger


def mask_query_password(query):
    # Preserve encoding, ordering, repeated parameters and empty values exactly.
    parts = re.split(r'([&;])', query)
    for index in range(0, len(parts), 2):
        key, separator, value = parts[index].partition('=')
        if separator and unquote_plus(key).lower() == 'password':
            parts[index] = key + '=[REDACTED]'
    return ''.join(parts)


def mask_url_password(url):
    path, separator, remainder = url.partition('?')
    if not separator:
        return url
    query, fragment_separator, fragment = remainder.partition('#')
    return (path + separator + mask_query_password(query)
            + fragment_separator + fragment)


class PasswordMaskingLogger(Logger):
    def atoms(self, resp, req, environ, request_time):
        # Copy for logging only: authentication still receives original values.
        safe_environ = environ.copy()
        for key in ('RAW_URI', 'REQUEST_URI', 'HTTP_REFERER'):
            if key in safe_environ:
                safe_environ[key] = mask_url_password(safe_environ[key])
        if 'QUERY_STRING' in safe_environ:
            safe_environ['QUERY_STRING'] = mask_query_password(safe_environ['QUERY_STRING'])
        atoms = super().atoms(resp, req, safe_environ, request_time)
        # Gunicorn also exposes headers as separate format atoms.
        if '{referer}i' in atoms:
            atoms['{referer}i'] = mask_url_password(atoms['{referer}i'])
        return atoms
