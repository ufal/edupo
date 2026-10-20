"""Offline route tests; no corpus, generators or external API calls required."""
import copy
import importlib
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

BACKEND = Path(__file__).resolve().parents[1] / 'backend'
sys.path.insert(0, str(BACKEND))
import poem_cache

with patch.object(poem_cache, 'init_cache_db'):
    previous = os.getcwd()
    try:
        os.chdir(BACKEND)
        backend = importlib.import_module('app')
    finally:
        os.chdir(previous)


class PasswordProtectionTests(unittest.TestCase):
    def setUp(self):
        self.passwords = patch.object(backend, 'HESLA', {'test-secret'})
        self.passwords.start()
        self.addCleanup(self.passwords.stop)
        self.client = backend.app.test_client()
        self.poem = {
            'id': 123, 'title': 'Example', 'author_name': 'Author',
            'copyrighted': 1,
            'plaintext': 'First line of the poem\nSECRET REST OF POEM',
            'verses': [{'text': 'First line of the poem'}, {'text': 'SECRET REST OF POEM'}],
            'body': [{'text': 'SECRET REST OF POEM'}],
            'translations': {'sk': 'SECRET TRANSLATION'},
            'rawtext': 'SECRET RAW OUTPUT',
        }
        self.loader = patch.object(backend, 'get_poem_by_id',
                                  side_effect=lambda **kw: copy.deepcopy(self.poem))
        self.loader.start()
        self.addCleanup(self.loader.stop)
        self.audit = tempfile.TemporaryDirectory()
        self.addCleanup(self.audit.cleanup)
        self.log = patch.object(backend, 'PWDLOG', str(Path(self.audit.name) / 'audit.log'))
        self.log.start()
        self.addCleanup(self.log.stop)

    def test_every_protected_route_denies_before_handler(self):
        routes = ['/typfeatures', '/search', '/translate', '/processopenai', '/openaigenerate', '/logs', '/showlist', '/genimage']
        for route in routes:
            for method in ['get', 'post']:
                for accept in ['html', 'json', 'txt']:
                    for password in [None, 'wrong']:
                        params = {'accept': accept}
                        if password is not None:
                            params['password'] = password
                        with self.subTest(route=route, method=method, accept=accept, password=password):
                            response = getattr(self.client, method)(
                                route, **({'query_string': params} if method == 'get' else {'data': params}))
                            self.assertEqual(response.status_code, 401)
                            self.assertIn('Unauthorized', response.text)
        self.assertFalse(backend.get_poem_by_id.called)

    def test_valid_credentials_reach_all_handlers(self):
        for endpoint in backend.PASSWORD_PROTECTED_ENDPOINTS:
            route = next(rule.rule for rule in backend.app.url_map.iter_rules()
                         if rule.endpoint == endpoint)
            with patch.dict(backend.app.view_functions, {endpoint: lambda: 'allowed'}):
                for kwargs in [dict(headers={'Authorization': 'Bearer test-secret'}),
                               dict(query_string={'password': 'test-secret'})]:
                    self.assertEqual(self.client.get(route, **kwargs).text, 'allowed')
                self.assertEqual(self.client.post(route, data={'password': 'test-secret'}).text, 'allowed')

    def test_login_cookie_logout_and_wrong_explicit_password(self):
        self.assertEqual(self.client.post('/login', data={'password': 'wrong'}).status_code, 401)
        response = self.client.post('/login', data={'password': 'test-secret'})
        self.assertEqual(response.status_code, 303)
        cookie = response.headers['Set-Cookie']
        self.assertNotIn('test-secret', cookie)
        self.assertIn('HttpOnly', cookie)
        self.assertIn('SameSite=Strict', cookie)
        with patch.dict(backend.app.view_functions, {'call_search': lambda: 'allowed'}):
            self.assertEqual(self.client.get('/search').text, 'allowed')
            self.assertEqual(self.client.get('/search?password=wrong').status_code, 401)
            self.client.post('/logout')
            self.assertEqual(self.client.get('/search').status_code, 401)

    def test_logs_link_and_cookie_authentication(self):
        self.assertNotIn('Zobrazit logy', self.client.get('/').text)
        self.client.post('/login', data={'password': 'test-secret'})
        page = self.client.get('/').text
        self.assertIn('href="/logs?accept=html"', page)
        self.assertNotIn('test-secret', page)
        with patch.dict(backend.app.view_functions, {'call_logs': lambda: 'log contents'}):
            response = self.client.get('/logs?accept=html')
            self.assertEqual(response.text, 'log contents')
            self.assertEqual(response.headers['Cache-Control'], 'private, no-store')
            self.client.post('/logout')
            self.assertEqual(self.client.get('/logs').status_code, 401)

    def test_show_copyright_preview_all_formats(self):
        for accept in ['json', 'txt', 'html']:
            response = self.client.get('/show', query_string={'accept': accept})
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.poem['plaintext'].split('\n')[0][:20], response.text)
            self.assertIn('autorsk', response.text)
            self.assertNotIn('SECRET', response.text)
            self.assertEqual(response.headers['Cache-Control'], 'private, no-store')
        data = self.client.get('/show?accept=json').json
        self.assertNotIn('body', data)
        self.assertNotIn('translations', data)

    def test_show_authorized_and_public_poems_keep_full_text(self):
        response = self.client.get('/show?accept=json', headers={'Authorization': 'Bearer test-secret'})
        self.assertIn('SECRET REST OF POEM', response.json['plaintext'])
        self.assertEqual(self.poem['copyrighted'], 1)
        self.assertNotIn('test-secret', (Path(self.audit.name) / 'audit.log').read_text())
        self.poem['copyrighted'] = 0
        self.assertIn('SECRET REST OF POEM', self.client.get('/show?accept=txt').text)

    def test_cookie_tampering_expiry_and_password_change(self):
        auth = backend.password_auth
        token = auth.serializer().dumps('authenticated')
        with backend.app.test_request_context(headers={'Cookie': f'{auth.cookie_name}={token}x'}):
            self.assertFalse(auth.authenticated())
        with backend.app.test_request_context(headers={'Cookie': f'{auth.cookie_name}={token}'}):
            with patch.object(auth, 'max_age', -1):
                self.assertFalse(auth.authenticated())
            with patch.object(backend, 'HESLA', {'replacement'}):
                self.assertFalse(auth.authenticated())
            with patch.object(backend, 'HESLA', set()):
                self.assertFalse(auth.authenticated())

    def test_showlist_and_genimage_use_login_cookie(self):
        self.client.post('/login', data={'password': 'test-secret'})
        for endpoint, route in [('call_showlist', '/showlist'), ('call_genimage', '/genimage')]:
            with patch.dict(backend.app.view_functions, {endpoint: lambda: 'allowed'}):
                self.assertEqual(self.client.get(route).text, 'allowed')
                self.assertEqual(self.client.get(route + '?password=wrong').status_code, 401)
        self.client.post('/logout')
        for route in ['/showlist', '/genimage']:
            self.assertEqual(self.client.get(route).status_code, 401)

    def test_production_cookie_scope_and_secure_flag(self):
        response = self.client.post('/api/login', base_url='https://edupo.cz',
                                    data={'password': 'test-secret'})
        self.assertEqual(response.status_code, 303)
        self.assertIn('Secure', response.headers['Set-Cookie'])
        self.assertIn('Path=/api', response.headers['Set-Cookie'])


if __name__ == '__main__':
    unittest.main()
