"""Offline checks of the actual Gunicorn access-log atoms."""
from datetime import timedelta
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'backend'))
from access_logging import PasswordMaskingLogger, mask_url_password


class AccessLoggingTests(unittest.TestCase):
    def test_urls_preserve_other_parameters(self):
        cases = [
            ('/show?poemid=123&password=secret&accept=json',
             '/show?poemid=123&password=[REDACTED]&accept=json'),
            ('/search?password=a&query=two%20words&password=b',
             '/search?password=[REDACTED]&query=two%20words&password=[REDACTED]'),
            ('/show?%70assword=a%26b%3Dc&PASSWORD=other',
             '/show?%70assword=[REDACTED]&PASSWORD=[REDACTED]'),
            ('/show?password=&poemid=123#section',
             '/show?password=[REDACTED]&poemid=123#section'),
            ('/show?poemid=123&accept=json', '/show?poemid=123&accept=json'),
            ('/show', '/show'),
        ]
        for original, expected in cases:
            with self.subTest(original=original):
                self.assertEqual(mask_url_password(original), expected)

    def test_gunicorn_format_masks_request_and_referrer(self):
        environ = {
            'REQUEST_METHOD': 'GET', 'RAW_URI': '/show?poemid=123&password=secret',
            'QUERY_STRING': 'poemid=123&password=secret', 'PATH_INFO': '/show',
            'SERVER_PROTOCOL': 'HTTP/1.1',
            'HTTP_REFERER': 'https://edupo.cz/api/?password=other-secret&accept=html',
            'HTTP_USER_AGENT': 'Test browser',
        }
        original = environ.copy()
        logger = PasswordMaskingLogger.__new__(PasswordMaskingLogger)
        atoms = logger.atoms(SimpleNamespace(status='200 OK', sent=123, headers=[]),
                             [('Referer', environ['HTTP_REFERER'])], environ, timedelta())
        self.assertEqual(atoms['r'], 'GET /show?poemid=123&password=[REDACTED] HTTP/1.1')
        self.assertEqual(atoms['f'], 'https://edupo.cz/api/?password=[REDACTED]&accept=html')
        self.assertEqual(atoms['a'], 'Test browser')
        self.assertEqual(atoms['q'], 'poemid=123&password=[REDACTED]')
        self.assertEqual(atoms['{referer}i'], atoms['f'])
        self.assertEqual(environ, original)
        # Both launch scripts must activate masking with their actual formats.
        root = Path(__file__).resolve().parents[1]
        for relative_path in ['backend/app.sh', 'deploy/start-backend.sh']:
            with self.subTest(script=relative_path):
                script = (root / relative_path).read_text()
                self.assertIn('--logger-class access_logging.PasswordMaskingLogger', script)
                log_format = script.split("--access-logformat '", 1)[1].split("'", 1)[0]
                output = log_format % logger.atoms_wrapper_class(atoms)
                self.assertNotIn('secret', output)
                self.assertIn('poemid=123', output)
                self.assertIn('Test browser', output)



if __name__ == '__main__':
    unittest.main()
